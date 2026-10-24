"""CSV-only pipeline and Technical Guardrails regression tests."""
from dataclasses import FrozenInstanceError, replace
import csv
from pathlib import Path
import unittest
from heat_pump_ready.config import AssessmentConfig
from heat_pump_ready.contracts import UserInput
from heat_pump_ready.intake import build_user_input, INPUT_COLUMNS
from heat_pump_ready.calculation.registry import build_modules
from heat_pump_ready.calculation.orchestrator import CalculationOrchestrator
from heat_pump_ready.demo_cases import CASES, SYNTHETIC
from heat_pump_ready.llm.runners import DisabledRunner
from heat_pump_ready.validator import validate_and_decide


class PipelineTests(unittest.TestCase):
    """Use actual CSV cases and independent known expected outputs."""

    def setUp(self):
        self.config = AssessmentConfig()
        self.input = build_user_input(SYNTHETIC)
        self.modules = build_modules(self.config, DisabledRunner())
        self.cases = {row['building_id']: build_user_input(row) for row in CASES}

    def run_case(self, user=None, disabled=()):
        return CalculationOrchestrator(self.modules, disabled).run(user or self.input)

    def test_contract_matches_eval_header_exactly(self):
        with (Path(__file__).parents[1] / 'heat_pump_ready/data/buildings_eval.csv').open(encoding='utf-8') as stream:
            self.assertEqual(tuple(next(csv.reader(stream))), INPUT_COLUMNS)
        import re
        html = (Path(__file__).parents[1] / 'heat_pump_ready/web/index.html').read_text(encoding='utf-8')
        names = re.findall(r'<(?:input|select|textarea)\b[^>]*\bname="([^"]+)"', html)
        self.assertEqual(set(names), set(INPUT_COLUMNS))
        self.assertEqual(len(names), 16)

    def test_no_extra_inputs_or_reference_labels(self):
        for key in ('tabula_profile', 'investment_eur', 'subsidy_eur', 'horizon_years', 'attachments',
                    'reference_heating_load_kw', 'expected_verdict', 'climate_region', 'consumption_unit',
                    'annual_consumption', 'hp_price_eur_kwh', 'annual_performance_factor'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                build_user_input({key: 1})
        for row in CASES:
            self.assertEqual(set(row), set(INPUT_COLUMNS))

    def test_csv_blanks_and_yes_are_preserved(self):
        for case in ('B-04', 'B-05'):
            self.assertEqual(self.cases[case].renovation_status, 'unknown')
            self.assertIsNone(self.cases[case].flow_temperature_c)
            self.assertTrue(self.cases[case].hot_water_via_heating)
        self.assertIsNone(self.cases['B-04'].rooms)
        self.assertEqual(self.cases['B-05'].rooms, 14)
        self.assertIsNone(build_user_input({'hot_water_via_heating': ''}).hot_water_via_heating)
        self.assertFalse(build_user_input({'hot_water_via_heating': 'no'}).hot_water_via_heating)

    def test_synthetic_heat_and_fixed_costs(self):
        out = self.run_case()
        self.assertEqual(out.useful_heat.value, 21120)
        self.assertEqual(out.space_heating_demand.value, 18120)
        self.assertEqual(out.heat_load_consumption.value, 9.06)
        self.assertEqual(out.current_energy_cost.value, 2640)
        self.assertAlmostEqual(out.heat_pump_energy_cost.value, 1568.9142857142856)
        self.assertAlmostEqual(out.annual_savings.value, 1071.0857142857144)
        self.assertEqual(out.net_investment.status, 'missing_input')
        self.assertEqual(out.payback_period.status, 'blocked')
        self.assertEqual(validate_and_decide(out, self.config).verdict, 'undetermined')

    def test_eval_b04_no_second_oil_conversion(self):
        out = self.run_case(self.cases['B-04'])
        self.assertEqual(out.annual_consumption.value, 25000)
        self.assertEqual(out.useful_heat.value, 22000)
        self.assertEqual(out.space_heating_demand.value, 19000)
        self.assertEqual(out.heat_load_consumption.value, 9.5)
        self.assertAlmostEqual(out.current_energy_cost.value, 4250)
        self.assertEqual(out.annual_performance_factor.status, 'missing_input')
        self.assertEqual(out.heat_pump_energy_cost.status, 'blocked')
        self.assertEqual(validate_and_decide(out,self.config,self.cases['B-04']).readiness, 'yellow')

    def test_eval_b05_no_invented_flow_or_solar_yield(self):
        user = self.cases['B-05'];out = self.run_case(user)
        self.assertEqual(out.annual_consumption.value, 27000)
        self.assertEqual(out.heat_load_consumption.value, 10.38)
        self.assertEqual(out.current_energy_cost.value, 2970)
        self.assertEqual(out.annual_performance_factor.status, 'missing_input')
        decision = validate_and_decide(out,self.config,user)
        self.assertEqual(decision.readiness, 'yellow')
        self.assertTrue(any('Solarthermie' in c for c in decision.technician_checks))

    def test_lpg_detail_never_uses_natural_gas_price(self):
        user = self.cases['B-01'];out = self.run_case(user)
        self.assertEqual(user.energy_carrier, 'gas')  # source fact is preserved
        self.assertEqual(out.current_energy_cost.status, 'missing_input')
        self.assertEqual(out.useful_heat.value, 8800)

    def test_fixed_jaz_boundaries_and_underfloor(self):
        self.assertEqual(self.config.hp_price_eur_kwh, 0.26)
        self.assertEqual(self.config.gas_price_eur_kwh, 0.11)
        self.assertEqual(self.config.oil_price_eur_kwh, 0.17)
        self.assertEqual(self.run_case(replace(self.input,heat_distribution='underfloor',flow_temperature_c=None)).annual_performance_factor.value, 4)
        for temperature,expected in ((55,3.5),(55.01,2.8),(60,2.8)):
            self.assertEqual(self.run_case(replace(self.input,flow_temperature_c=temperature)).annual_performance_factor.value,expected)
        self.assertEqual(self.run_case(replace(self.input,flow_temperature_c=61)).annual_performance_factor.status,'missing_input')

    def test_separate_warm_water_keeps_total_cost_scope(self):
        out = self.run_case(replace(self.input,hot_water_via_heating=False))
        self.assertEqual(out.hot_water_demand.value, 0)
        self.assertEqual(out.space_heating_demand.value, 21120)
        self.assertEqual(out.heat_pump_energy_cost.value,self.run_case().heat_pump_energy_cost.value)
        missing = self.run_case(replace(self.input,hot_water_via_heating=None))
        self.assertEqual(missing.heat_load_consumption.status,'blocked')
        self.assertEqual(missing.heat_pump_energy_cost.status,'available')

    def test_missing_consumption_is_not_filled_from_tabula(self):
        out = self.run_case(replace(self.input,annual_consumption_kwh=None))
        self.assertEqual(out.tabula_space_heating_demand.status,'available')
        self.assertEqual(out.annual_consumption.status,'missing_input')
        self.assertEqual(out.heat_pump_energy_cost.status,'blocked')

    def test_disabled_producer_blocks_only_dependents(self):
        out=self.run_case(disabled=('annual_consumption',))
        self.assertEqual(out.useful_heat.status,'blocked')
        self.assertEqual(out.heat_load_range.status,'blocked')
        self.assertEqual(out.heat_load_area.status,'available')
        self.assertEqual(out.tabula_space_heating_demand.status,'available')

    def test_range_and_no_silent_average(self):
        out=self.run_case()
        self.assertEqual(out.heat_load_range.value, (7.2,10.8))
        self.assertEqual(out.heat_load_consumption.value,9.06)

    def test_inconsistent_values_prevent_positive_assessment(self):
        out=self.run_case(replace(self.input,annual_consumption_kwh=100))
        self.assertLess(out.space_heating_demand.value,0)
        self.assertTrue(validate_and_decide(out,self.config).validation_issues)

    def test_pipe_and_radiator_evidence_is_not_fabricated(self):
        out=self.run_case(replace(self.input,pipe_system='unknown',radiator_info='12 radiators with valve blocks; type and age not documented'))
        self.assertEqual(out.pipe_system.status,'missing_input')
        self.assertEqual(out.radiator_type.status,'missing_input')
        documented=self.run_case(replace(self.input,radiator_info='Type 22 panel radiator'))
        self.assertEqual(documented.radiator_type.value,'22')
        self.assertIsNotNone(documented.radiator_type.uncertainty)

    def test_green_requires_some_heat_load_evidence(self):
        out=self.run_case(disabled=('heat_load_consumption','heat_load_area'))
        self.assertEqual(validate_and_decide(out,self.config).readiness,'yellow')

    def test_specific_load_hint_is_not_exclusion(self):
        user=replace(self.input,floor_area_m2=100,annual_consumption_kwh=25000)
        decision=validate_and_decide(self.run_case(user),self.config,user)
        self.assertTrue(any('75 W/m²' in r for r in decision.reasons))
        self.assertEqual(decision.readiness,'green')

    def test_immutability_and_registry_contracts(self):
        with self.assertRaises(FrozenInstanceError):self.input.floor_area_m2=1
        with self.assertRaises(ValueError):CalculationOrchestrator(self.modules+(self.modules[0],))
        with self.assertRaises(ValueError):CalculationOrchestrator(tuple(reversed(self.modules)))
        out=CalculationOrchestrator(self.modules[1:]).run(self.input)
        self.assertEqual(out.annual_consumption.status,'disabled')
        self.assertEqual(out.useful_heat.status,'blocked')

    def test_numeric_validation_and_true_zero(self):
        for data in ({'floor_area_m2':'nan'},{'annual_consumption_kwh':True},{'persons_in_household':2.5},
                     {'hot_water_via_heating':'perhaps'},{'rooms':0},{'energy_carrier':[]}):
            with self.subTest(data=data),self.assertRaises(ValueError):build_user_input(data)
        self.assertEqual(self.run_case(replace(self.input,annual_consumption_kwh=0)).annual_consumption.value,0)


if __name__=='__main__':unittest.main()

from lcls_live.datamaps.impact import get_impact_datamaps


def test_cu_inj():
    _test_datamap(
        "cu_inj",
        {
            # pvname_rbv or pvname: [impact_name, impact_attribute, impact_factor, impact_unit]
            "SOLN:IN20:121:BACT": ["SOL1", "solenoid_field_scale", 0.51427242, "T"],
            "QUAD:IN20:121:BACT": ["CQ01", "b1_gradient", -0.476190476, "T/m"],
            "QUAD:IN20:122:BACT": ["SQ01", "b1_gradient", -0.476190476, "T/m"],
            "ACCL:IN20:300:L0A_PDES": ["L0A_phase", "dtheta0_deg", 1.0, "deg"],
            "ACCL:IN20:400:L0B_PDES": ["L0B_phase", "dtheta0_deg", 1.0, "deg"],
            "ACCL:IN20:300:L0A_ADES": ["L0A_scale", "voltage", 1000000.0, "V"],
            "ACCL:IN20:400:L0B_ADES": ["L0B_scale", "voltage", 1000000.0, "V"],
            "QUAD:IN20:361:BACT": ["QA01", "b1_gradient", -0.925925926, "T/m"],
            "QUAD:IN20:371:BACT": ["QA02", "b1_gradient", -0.925925926, "T/m"],
            "BPMS:IN20:221:TMIT1H": ["", "total_charge", 1.602176634e-19, "C"],
        },
    )


def test_sc_inj():
    _test_datamap(
        "sc_inj",
        {
            # pvname_rbv or pvname: [impact_name, impact_attribute, impact_factor, impact_unit]
            "SOLN:GUNB:212:BACT": ["SOL1B", "solenoid_field_scale", 1.159555403, "T"],
            "SOLN:GUNB:823:BACT": ["SOL2B", "solenoid_field_scale", 1.159555403, "T"],
            "BPMS:GUNB:314:TMIT": ["", "total_charge", 1.602176634e-19, "C"],
            "ACCL:L0B:0110:AACTMEAN": [
                "CAVL011",
                "rf_field_scale",
                1861947.347098133,
                "V/m",
            ],
            "ACCL:L0B:0180:AACTMEAN": [
                "CAVL018",
                "rf_field_scale",
                1861947.347098133,
                "V/m",
            ],
            "ACCL:L0B:0110:PACTMEAN": ["CAVL011", "autophase_deg", 1, "deg"],
            "ACCL:L0B:0180:PACTMEAN": ["CAVL018", "autophase_deg", 1, "deg"],
            "QUAD:HTR:120:BACT": ["Q0H01", "b1_gradient", -0.803858521, "T/m"],
            "QUAD:HTR:460:BACT": ["Q0H08", "b1_gradient", -0.803858521, "T/m"],
        },
    )


def _test_datamap(model, expect):
    def _round(attribute, value):
        if attribute == "total_charge":
            return round(value, 28)
        return round(value, 9)

    for name, dm in get_impact_datamaps(model).items():
        for row in dm.data.itertuples():
            pv = getattr(row, "pvname_rbv", row.pvname)
            if pv in expect:
                a = [
                    row.impact_name,
                    row.impact_attribute,
                    _round(row.impact_attribute, row.impact_factor),
                    row.impact_unit,
                ]
                assert expect[pv] == a, f"{expect[pv]} != {a}"
                del expect[pv]
    assert not len(expect), f"leftover test cases: {expect}"

# from flow_cytometry import make_samples
import importlib
import pytest
import json
from autoprotocol import Protocol, Container


@pytest.fixture(scope='session')
def flow_cytometry():
    loader = importlib.machinery.SourceFileLoader(
        'flow_cytometry', 'flow_cytometry.py')
    spec = importlib.util.spec_from_loader(loader.name, loader)
    flow_cytometry = importlib.util.module_from_spec(spec)
    loader.exec_module(flow_cytometry)
    return flow_cytometry


def test_make_samples(flow_cytometry):
    p = Protocol()
    plate = p.ref("sample_plate_1",
                  cont_type="96-flat",
                  discard=True)
    wells = plate.all_wells()
    assert len(flow_cytometry.make_samples(wells, "10:microliter")) == 96


def test_make_controls(flow_cytometry):
    pass


def test_flow_cytometry_runs_only_one_instruction(flow_cytometry):
    preview_data = '''
    {
        "refs": {
            "src_plate": {
                "type": "96-flat",
                "aliquots": {
                      "0": {"volume": "100:microliter"},
                      "1": {"volume": "100:microliter"},
                      "2": {"volume": "100:microliter"},
                      "3": {"volume": "100:microliter"},
                      "4": {"volume": "100:microliter"},
                      "5": {"volume": "100:microliter"},
                      "6": {"volume": "100:microliter"},
                      "7": {"volume": "100:microliter"}
                },
                "discard":true
            }
        },
        "parameters": {
            "fsc":{
                "area": true,
                "height": true,
                "weight": true
            },
            "ssc":{
                "area": true,
                "height": false,
                "weight": false
            },
            "color": "FitC, TxR",
            "pc_samples" : [{
                    "well" : "src_plate/1",
                    "vol" : "50:microliter",
                    "channel" : "FitC",
                    "events" : "1000",
                    "bleed" : [{
                      "from" : "FitC",
                      "to" : "TxR"
                    }]
            }],
            "nc_samples" : [{
                "well" : "src_plate/1",
                "vol" : "50:microliter",
                "events" : "1000",
                "channel" : "FSC,SSC,FitC,TxR"
            }],
            "samples" : {
                "well" : ["src_plate/2","src_plate/3","src_plate/4","src_plate/5","src_plate/6","src_plate/7"],
                "vol" : "50:microliter"
        }
      }
    }
    '''

    preview = (json.loads(preview_data))
    params = preview["parameters"]

    ref = Protocol().ref(name="src_plate", cont_type="96-flat", discard=True)
    for well in ref.wells_from(0,8):
        well.set_volume("100:microliter")

    params["samples"]["well"] = list(ref.wells_from(1,7))
    params["nc_samples"][0]["well"] = ref.well(0)
    params["pc_samples"][0]["well"] = ref.well(0)

    protocol = Protocol()
    flow_cytometry.flow_cytometry(protocol, params)
    assert len(protocol.as_dict()["instructions"]) == 1

import importlib
import pytest
import json
from autoprotocol.harness import get_protocol_preview
from autoprotocol import Protocol, Container, Well, WellGroup


@pytest.fixture(scope="module")
def preview():
    protocol = Protocol()
    preview = get_protocol_preview(protocol, "FlowCytometry", "manifest.json")
    return preview


@pytest.fixture(scope='session')
def flow_cytometry():
    loader = importlib.machinery.SourceFileLoader(
        'flow_cytometry', 'flow_cytometry.py')
    spec = importlib.util.spec_from_loader(loader.name, loader)
    flow_cytometry = importlib.util.module_from_spec(spec)
    loader.exec_module(flow_cytometry)
    return flow_cytometry


def test_preview(preview, flow_cytometry):
    protocol = Protocol()
    ref = Protocol().ref(name="src_plate", cont_type="96-flat", discard=True)
    for well in ref.wells_from(0, 8):
        well.set_volume("100:microliter")

    preview["samples"]["well"] = list(ref.wells_from(1, 7))
    preview["nc_samples"][0]["well"] = ref.well(0)
    preview["pc_samples"][0]["well"] = ref.well(0)
    preview["containers"] = [ref]
    flow_cytometry.flow_cytometry(protocol, params=preview)

    assert len(protocol.as_dict()["instructions"]) == 1


def test_protocol_removes_lids(preview, flow_cytometry):
    ref = Protocol().ref(name="src_plate", cont_type="96-flat", cover="universal", discard=True)
    for well in ref.wells_from(0, 8):
        well.set_volume("100:microliter")

    preview["samples"]["well"] = list(ref.wells_from(1, 7))
    preview["nc_samples"][0]["well"] = ref.well(0)
    preview["pc_samples"][0]["well"] = ref.well(0)

    protocol = Protocol()
    flow_cytometry.flow_cytometry(protocol, params=preview)

    operations = []
    for instruction in protocol.instructions:
        operations.append(instruction.op)
    print(operations)
    assert 'uncover' in operations


def test_make_samples_returns_the_correct_length(flow_cytometry):
    p = Protocol()
    plate = p.ref("sample_plate_1",
                  cont_type="96-flat",
                  discard=True)
    wells = plate.all_wells()
    assert len(flow_cytometry.make_samples(wells, "10:microliter")) == 96


def test_make_samples_returns_wells_and_volumes(flow_cytometry):
    p = Protocol()
    plate = p.ref("sample_plate_1",
                  cont_type="96-flat",
                  discard=True)
    wells = plate.all_wells()
    output = flow_cytometry.make_samples(wells, "10:microliter")
    assert isinstance(output[0]["well"], Well)
    assert isinstance(output[0]["volume"], str)


def test_make_samples_raises_type_error(flow_cytometry):
    p = Protocol()
    plate = p.ref("sample_plate_1",
                  cont_type="96-flat",
                  discard=True)
    wells = ["A1", "A2", "A3", 4, 5, 6]

    with pytest.raises(TypeError):
        output = flow_cytometry.make_samples(wells, "10:microliter")


def test_flow_cytometry_protocol_contains_flow_analyze_instruction(preview, flow_cytometry):
    ref = Protocol().ref(name="src_plate", cont_type="96-flat", discard=True)
    for well in ref.wells_from(0, 8):
        well.set_volume("100:microliter")

    preview["samples"]["well"] = list(ref.wells_from(1, 7))
    preview["nc_samples"][0]["well"] = ref.well(0)
    preview["pc_samples"][0]["well"] = ref.well(0)

    protocol = Protocol()
    flow_cytometry.flow_cytometry(protocol, params=preview)

    operations = []
    for instruction in protocol.instructions:
        operations.append(instruction.op)
    assert 'flow_analyze' in operations


def test_make_controls_raises_type_error_on_argument(flow_cytometry):
    p = Protocol()
    plate = p.ref("sample_plate_1",
                  cont_type="96-flat",
                  discard=True)
    wells = plate.all_wells()
    with pytest.raises(TypeError):
        output = flow_cytometry.make_controls(wells)


def test_make_controls_returns_listof_dicts(flow_cytometry):
    p = Protocol()
    plate = p.ref("sample_plate_1",
                  cont_type="96-flat",
                  discard=True)
    controls = [
        {
            'well': plate.well(0),
            'vol': "50:microliter",
            'events': None,
            'channel': 'FSC,SSC,FitC,TxR'
        }
    ]
    output = flow_cytometry.make_controls(controls)

    assert isinstance(output, list)
    assert isinstance(output[0], dict)


def test_flow_cytometry_runs_only_one_instruction(preview, flow_cytometry):
    ref = Protocol().ref(name="src_plate", cont_type="96-flat", discard=True)
    for well in ref.wells_from(0, 8):
        well.set_volume("100:microliter")

    preview["samples"]["well"] = list(ref.wells_from(1, 7))
    preview["nc_samples"][0]["well"] = ref.well(0)
    preview["pc_samples"][0]["well"] = ref.well(0)

    protocol = Protocol()
    flow_cytometry.flow_cytometry(protocol, params=preview)
    assert len(protocol.as_dict()["instructions"]) == 1

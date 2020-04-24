from autoprotocol.container import Container, WellGroup
from autoprotocol.protocol import Ref
from autoprotocol.unit import Unit
import datetime


def printdatetime(time=True):
    printdate = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    if not time:
        printdate = datetime.datetime.now().strftime('%Y-%m-%d')
    return printdate

def provision_to_tube(protocol, name, tube, resource_id, volume, discard=True, storage=None):
    '''
        provision_to_tube allows us to provision into a tube/well that can then be used
        in transfers on the workcell.
    '''
    assert isinstance(volume, (Unit, int, float)), "Volume must be of type int, float or Unit."
    if isinstance(volume, Unit):
        volume = volume.value
    if storage:
        dest = protocol.ref(name, None, tube, storage=storage).well(0)
    else:
        dest = protocol.ref(name, None, tube, discard=discard).well(0)
    protocol.provision(resource_id, dest, "%s:microliter" % volume)
    return(dest)


def ref_kit_container(protocol, name, container, kit_id, discard=True, store=None):
    '''
        Still in use to allow booking of agar plates on the fly
    '''
    kit_item = Container(None, protocol.container_type(container), name)
    if store:
        protocol.refs[name] = Ref(name, {"reserve": kit_id, "store": {"where": store}}, kit_item)
    else:
        protocol.refs[name] = Ref(name, {"reserve": kit_id, "discard": discard}, kit_item)
    return(kit_item)


def make_list(my_str, integer=False):
    '''
        Sometimes you need a list of a type that is not supported. This takes a string and
        comma-seperates it, returning a list of strings or integers.
    '''
    assert isinstance(my_str, str), "Input needs to be of type string."
    if integer:
        my_str = [int(x.strip()) for x in my_str.split(",")]
    else:
        my_str = [x.strip() for x in my_str.split(",")]
    return my_str


def thermocycle_ramp(start_temp, end_temp, total_duration, step_duration):
    '''
        Create a ramp instruction for the thermocyler. Used in annealing protocols.
    '''
    assert Unit.fromstring(total_duration).unit == Unit.fromstring(step_duration).unit, ("Thermocycle_ramp durations"
                                                                                         " must be specified using the"
                                                                                         " same unit of time.")
    thermocycle_steps = []
    start_temp = Unit.fromstring(start_temp).value
    num_steps = int(Unit.fromstring(total_duration).value // Unit.fromstring(step_duration).value)
    step_size = (Unit.fromstring(end_temp).value - start_temp) // num_steps
    for i in range(0, num_steps):
        thermocycle_steps.append({
            "temperature": "%d:celsius" % (start_temp + i * step_size), "duration": step_duration
            })
    return thermocycle_steps


def return_agar_plates(wells):
    '''
        Dicts of all plates available that can be purchased.
    '''
    if wells == 6:
        plates = {"50_ug/ml_Kanamycin": "ki17rs7j799zc2",
                  "100_ug/ml_Ampicillin": "ki17sbb845ssx9",
                  "100_ug/mL_Spectinomycin": "ki17sbb9r7jf98",
                  "noAB": "ki17reefwqq3sq"}
    elif wells == 1:
        plates = {"50_ug/ml_Kanamycin": "ki17t8j7kkzc4g",
                  "100_ug/ml_Ampicillin": "ki17sbb845ssx9",
                  "100_ug/mL_Spectinomycin": "ki17t8jcebshtr",
                  "noAB": "ki17t8jejbea4z"}
    else:
        raise ValueError("Wells has to be an integer, either 1 or 6")
    return(plates)


def det_new_group(i, base=0):
    '''
        Helper to determine if new_group should be added. Returns true when i matches the base, which defaults to 0.
    '''
    assert isinstance(i, int), "Needs an integer."
    assert isinstance(base, int), "Base has to be an integer"
    if i == base:
        new_group = True
    else:
        new_group = False
    return new_group


def return_dispense_media():
    '''
        Dict of media for reagent dispenser
    '''
    media = {"50_ug/ml_Kanamycin": "lb-broth-50ug-ml-kan",
             "100_ug/ml_Ampicillin": "lb-broth-100ug-ml-amp",
             "100_ug/mL_Spectinomycin": "lb-broth-100ug-ml-specto",
             "30_ug/ml_Kanamycin": "lb-broth-30ug-ml-kan",
             "50_ug/ml_Kanamycin_25_ug/ml_Chloramphenicol": "lb-broth-50ug-ml-kan-25ug-ml-cm",
             "15_ug/ml_Tetracycline": "lb-broth-15ug-ml-tet",
             "25_ug/ml_Chloramphenicol": "lb-broth-25ug-ml-cm",
             "LB_broth": "lb-broth-noAB"}
    return(media)


def serial_dilute_rowwise(protocol, source, well_group, vol,
                          mix_after=True, reverse=False):
        """
        Serial dilute source liquid in specified wells of the container
        specified. Defaults to dilute from left to right (increasing well index)
        unless reverse is set to true.  This operation utilizes the transfers()
        method on Pipette, meaning only one tip is used.  All wells in the
        WellGroup well_group except for the first and last well should already
        contain the diluent.

        Example Usage:

        .. code-block:: python

            p = Protocol()
            sample_plate = p.ref("sample_plate",
                                 None,
                                 "96-flat",
                                 storage="warm_37")
            sample_source = p.ref("sample_source",
                                  "ct32kj234l21g",
                                  "micro-1.5",
                                  storage="cold_20")

            p.serial_dilute_rowwise(sample_source.well(0),
                                    sample_plate.wells_from(0,12),
                                    "50:microliter",
                                    mix_after=True)

        Parameters
        ----------
        container : Container
        source : Well
            Well containing source liquid.  Will be transfered to starting well,
            with double the volume specified in parameters
        start_well : Well
            Start of dilution, well containing the highest concentration of
            liquid
        end_well : Well
            End of dilution, well containing the lowest concentration of liquid
        vol : Unit, str
            Final volume of each well in the dilution series, most concentrated
            liquid will be transfered to the starting well with double this
            volume
        mix_after : bool, optional
            If set to True, each well will be mixed after liquid is transfered
            to it.
        reverse : bool, optional
            If set to True, liquid will be most concentrated in the well in the
            dilution series with the highest index

        """
        if not isinstance(well_group, WellGroup):
            raise RuntimeError("serial_dilute_rowwise() must take a WellGroup "
                               "as an argument")
        source_well = well_group.wells[0]
        begin_dilute = well_group.wells[0]
        end_dilute = well_group.wells[-1]
        wells_to_dilute = well_group[0].container.wells_from(begin_dilute,
                                    end_dilute.index-begin_dilute.index + 1)
        srcs = WellGroup([])
        dests = WellGroup([])
        vols = []
        if reverse:
            source_well = well_group.wells[-1]
            begin_dilute = well_group.wells[-1]
            end_dilute = well_group.wells[0]
            wells_to_dilute = well_group[0].container.wells_from(end_dilute,
                                    begin_dilute.index-end_dilute.index + 1)
        protocol.transfer(source.set_volume(Unit.fromstring(vol)*2),
                          source_well,
                          Unit.fromstring(vol)*2)
        if reverse:
            while len(wells_to_dilute.wells) >= 2:
                srcs.append(wells_to_dilute.wells.pop())
                dests.append(wells_to_dilute.wells[-1])
                vols.append(vol)
        else:
            for i in range(1, len(wells_to_dilute.wells)):
                srcs.append(wells_to_dilute.wells[i-1])
                dests.append(wells_to_dilute[i])
                vols.append(vol)
        protocol.transfer(srcs.set_volume(Unit.fromstring(vol)*2), dests, vols,
                          mix_after=mix_after, one_tip=True)

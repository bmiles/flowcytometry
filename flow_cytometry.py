import datetime
from autoprotocol_utilities.misc_helpers import make_list
from autoprotocol.container import Well, WellGroup


def make_samples(wells, volume):
    if isinstance(wells, (WellGroup, list)) and isinstance(wells[0], Well):
        return [{
            "well": well,
            "volume": volume
        } for well in wells]
    else:
        raise TypeError(f"{type(wells)}, should be of type WellGroup or list of well")


def make_controls(controls):
    """Receives a WellGroup and assembles an list of dicts called targets."""
    if isinstance(controls, (WellGroup, list)):
        targets = []

        for control in controls:
            control = dict(control)
            control["channel"] = make_list(control["channel"])
            if "bleed" in control:
                bleed = [{"from": bl["from"], "to": make_list(bl["to"])} for bl in control["bleed"]]
                if control["events"]:
                    targets.append({
                        "well": control["well"],
                        "volume": control["vol"],
                        "events": control["events"],
                        "channel": control["channel"],
                        "minimize_bleed": bleed
                    })
                else:
                    targets.append({
                        "well": control["well"],
                        "volume": control["vol"],
                        "channel": control["channel"],
                        "minimize_bleed": bleed
                    })
            else:
                if control["events"]:
                    targets.append({"well": control["well"], "volume": control["vol"], "events": control["events"],
                                    "channel": control["channel"]})
                else:
                    targets.append({"well": control["well"], "volume": control["vol"], "channel": control["channel"]})

        return targets
    else:
        raise TypeError(f"{type(controls)}, should be of type WellGroup or list of well")

def flow_cytometry(protocol, params):
    params = dict(params)
    params["samples"] = dict(params["samples"])
    params["color"] = make_list(params["color"])

    avail_colors = {
        "FitC": {"name": "FitC", "ex_wl": "488:nanometer", "em_wl": "530:nanometer"},
        "TxR": {"name": "TxR", "ex_wl": "561:nanometer", "em_wl": "620:nanometer"},
        "RFP": {"name": "RFP", "ex_wl": "561:nanometer", "em_wl": "583:nanometer"},
        "EYFP": {"name": "EYFP", "ex_wl": "488:nanometer", "em_wl": "574:nanometer"},
        "Pacific Blue": {"name": "Pacific Blue", "ex_wl": "405:nanometer", "em_wl": "440:nanometer"},
        "Pacific Green": {"name": "Pacific Green", "ex_wl": "405:nanometer", "em_wl": "512:nanometer"},
        "Pacific Orange": {"name": "Pacific Orange", "ex_wl": "405:nanometer", "em_wl": "603:nanometer"},
        "Qdot 705": {"name": "Qdot 705", "ex_wl": "405:nanometer", "em_wl": "710:nanometer"},
        "PerCP-Cy55": {"name": "PerCP-Cy5.5", "ex_wl": "488:nanometer", "em_wl": "695:nanometer"},
        "PeCy55": {"name": "PeCy55", "ex_wl": "561:nanometer", "em_wl": "695:nanometer"},
        "PeCy7": {"name": "PeCy7", "ex_wl": "561:nanometer", "em_wl": "780:nanometer"},
        "APC": {"name": "APC", "ex_wl": "638:nanometer", "em_wl": "660:nanometer"},
        "AlexaFluor750": {"name": "AlexaFluor750", "ex_wl": "638:nanometer", "em_wl": "780:nanometer"},
        "AlexaFluor700": {"name": "AlexaFluor700", "ex_wl": "638:nanometer", "em_wl": "720:nanometer"}
    }

    colors = [{
        "name": avail_colors[selected]["name"],
        "emission_wavelength": avail_colors[selected]["em_wl"],
        "excitation_wavelength": avail_colors[selected]["ex_wl"],
        "voltage_range": {"low": "200:volt", "high": "500:volt"},
        "area": True,
        "height": False,
        "weight": False
    } for selected in params["color"]]

    print(type(params["nc_samples"]))

    protocol.flow_analyze(
        dataref=datetime.date.today().strftime('%d%b%Y') + "_flow_" + str(len(params["samples"])) + "_samples",
        FSC={
            "voltage_range": {"low": "250:volt", "high": "450:volt"},
            "area": params["fsc"]['area'],
            "height": params["fsc"]['height'],
            "weight": params["fsc"]['weight']
        },
        SSC={
            "voltage_range": {"low": "250:volt", "high": "400:volt"},
            "area": params["ssc"]['area'],
            "height": params["ssc"]['height'],
            "weight": params["ssc"]['weight']
        },
        colors=colors,
        neg_controls=make_controls(params["nc_samples"]),
        pos_controls=make_controls(params["pc_samples"]),
        samples=make_samples(params["samples"]["well"], params["samples"]["vol"])
    )

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(flow_cytometry, "FlowCytometry")

from PyQt5.QtWidgets import QWidget
from . import subsystem_view
from rti_python.ADCP import AdcpCommands as Commands
from rti_python.ADCP.Predictor import DataStorage as DS
from rti_python.ADCP.Predictor import MaxVelocity as Velocity
from rti_python.ADCP.Predictor import Power as Power
from rti_python.ADCP.Predictor import Range as Range
from rti_python.ADCP.Predictor import STD as STD
from rti_python.ADCP import Subsystem as SS
from . import AdcpJson as JSON


class SubsystemVM(subsystem_view.Ui_Subsystem, QWidget):
    """
    Subsystem settings.
    """

    def __init__(self, parent, predictor, ss_code, ss_vm_clone):
        """
        Initialize the ViewModel.  If ss_vm_clone is None, then create a default
        configuration.  If ss_vm_clone is a value, then we are cloning a VM.
        :param parent: Tab Parent window.
        :param predictor: Predictor VM.
        :param ss_code: Subsystem code.
        :param ss_vm_clone: If cloning a VM, this value will not be None.
        """
        subsystem_view.Ui_Subsystem.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.predictor = predictor
        self.ss_code = ss_code
        self.freq = SS.ss_frequency(ss_code)

        # Set the label
        #self.freqLabel.setText("[" + str(ss_code) + "] - " + SS.ss_label(ss_code))

        # Set the style
        #self.freqLabel.setStyleSheet("font-weight: bold; color: red; font-size: 16px")
        #self.pingingTextBrowser.setStyleSheet("font-size: 10pt; color: white; background-color: transparent")
        #self.errorTextBrowser.setStyleSheet("font-size: 10pt; color: white; background-color: transparent")
        #self.powerLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.numBatteriesLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.wpRangeLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.btRangeLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.firstBinPosLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.maxVelLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.dataUsageLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.stdLabel.setStyleSheet("color: black; font-size: 12pt")
        #self.predictionGroupBox.setStyleSheet("QGroupBox#predictionGroupBox { background: #639ecf }\n QGroupBox::title { background-color: transparent; }")
        #self.statusGroupBox.setStyleSheet("QGroupBox { background: #3D9970 }\n QGroupBox::title { background-color: transparent; }")
        #self.errorGroupBox.setStyleSheet("QGroupBox { background: #cf6363 }\n QGroupBox::title { background-color: transparent; }")

        # Set the values based off the preset
        self.presetButton.clicked.connect(self.set_preset)

        # Clone the VM settings
        self.cloneButton.clicked.connect(self.clone_me)

        # Calculated results
        self.calc_power = 0.0
        self.calc_data = 0.0
        self.calc_ens_size = 0.0
        self.calc_num_batt = 0.0
        self.calc_max_vel = 0.0
        self.calc_std = 0.0
        self.calc_first_bin = 0.0
        self.calc_wp_range = 0.0
        self.calc_bt_range = 0.0
        self.calc_cfg_wp_range = 0.0

        # Initialize
        self.init_list()
        self.set_tooltips()

        # Set the checkbox state to enable and disable fields
        self.cwponCheckBox.stateChanged.connect(self.cwpon_enable_disable)
        self.cbtonCheckBox.stateChanged.connect(self.cbton_enable_disable)
        self.cbiEnabledCheckBox.stateChanged.connect(self.cbi_enable_disable)
        self.rangeTrackingComboBox.currentIndexChanged.connect(self.cwprt_enable_disable)

        # Clone or set default config
        if ss_vm_clone is not None:
            # Clone the config
            self.clone_config(ss_vm_clone)
        else:
            # Set default config
            self.set_default_config()

        # Watch for changes to recalculate
        self.cedBeamVelCheckBox.stateChanged.connect(self.stateChanged)
        self.cedInstrVelCheckBox.stateChanged.connect(self.stateChanged)
        self.cedEarthVelCheckBox.stateChanged.connect(self.stateChanged)
        self.cedAmpCheckBox.stateChanged.connect(self.stateChanged)
        self.cedCorrCheckBox.stateChanged.connect(self.stateChanged)
        self.cedBeamGoodPingCheckBox.stateChanged.connect(self.stateChanged)
        self.cedEarthGoodPingCheckBox.stateChanged.connect(self.stateChanged)
        self.cedEnsCheckBox.stateChanged.connect(self.stateChanged)
        self.cedAncCheckBox.stateChanged.connect(self.stateChanged)
        self.cedBtCheckBox.stateChanged.connect(self.stateChanged)
        self.cedNmeaCheckBox.stateChanged.connect(self.stateChanged)
        self.cedWpEngCheckBox.stateChanged.connect(self.stateChanged)
        self.cedBtEngCheckBox.stateChanged.connect(self.stateChanged)
        self.cedSysSettingCheckBox.stateChanged.connect(self.stateChanged)
        self.cedRangeTrackingCheckBox.stateChanged.connect(self.stateChanged)
        self.cwpblDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbsDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbnSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbbDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbbComboBox.currentIndexChanged.connect(self.valueChanged)
        self.cwppSpinBox.valueChanged.connect(self.valueChanged)
        self.cwptbpDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cbtbbComboBox.currentIndexChanged.connect(self.valueChanged)
        self.cbttbpDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cbiBurstIntervalDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cbiNumEnsSpinBox.valueChanged.connect(self.valueChanged)
        self.cbiInterleaveSpinBox.valueChanged.connect(self.valueChanged)
        self.numBeamsSpinBox.valueChanged.connect(self.valueChanged)
        self.cwprtRangeFractionSpinBox.valueChanged.connect(self.valueChanged)
        self.cwprtMinBinSpinBox.valueChanged.connect(self.valueChanged)
        self.cwprtMaxBinSpinBox.valueChanged.connect(self.valueChanged)
        self.beamDiaComboBox.currentIndexChanged.connect(self.stateChanged)
        self.beamAngleComboBox.currentIndexChanged.connect(self.stateChanged)

        # Show initial results
        self.calculate()

    def set_default_config(self):
        """
        Set the default configuration for the subsystem.
        :return:
        """
        # Init defaults
        self.cwponCheckBox.setCheckState(2)
        self.cbtonCheckBox.setCheckState(0)
        self.cbton_enable_disable(0)                    # Disable CBTON by default
        self.cbiEnabledCheckBox.setCheckState(0)
        self.cbi_enable_disable(0)                      # Disable CBI by default
        self.cedBeamVelCheckBox.setCheckState(2)
        self.cedInstrVelCheckBox.setCheckState(2)
        self.cedEarthVelCheckBox.setCheckState(2)
        self.cedAmpCheckBox.setCheckState(2)
        self.cedCorrCheckBox.setCheckState(2)
        self.cedBeamGoodPingCheckBox.setCheckState(2)
        self.cedEarthGoodPingCheckBox.setCheckState(2)
        self.cedEnsCheckBox.setCheckState(2)
        self.cedAncCheckBox.setCheckState(2)
        self.cedBtCheckBox.setCheckState(2)
        self.cedNmeaCheckBox.setCheckState(2)
        self.cedWpEngCheckBox.setCheckState(2)
        self.cedBtEngCheckBox.setCheckState(2)
        self.cedSysSettingCheckBox.setCheckState(2)
        self.cedRangeTrackingCheckBox.setCheckState(2)

        # Disable certain data types if PD0
        if self.predictor.dataFormatComboBox.currentText() == "RTB":
            self.cedWpEngCheckBox.setDisabled(False)
            self.cedBtEngCheckBox.setDisabled(False)
            self.cedSysSettingCheckBox.setDisabled(False)
            self.cedRangeTrackingCheckBox.setDisabled(False)
        else:
            self.cedWpEngCheckBox.setDisabled(True)
            self.cedBtEngCheckBox.setDisabled(True)
            self.cedSysSettingCheckBox.setDisabled(True)
            self.cedRangeTrackingCheckBox.setDisabled(True)

        # Check SS code to know how many beams
        if self.ss_code == 'A' or self.ss_code == 'B' or self.ss_code == 'C' or self.ss_code == 'D' or self.ss_code == 'E':
            self.numBeamsSpinBox.setValue(1)
            self.beamAngleComboBox.setCurrentIndex(1)       # 0 Degrees

        # Check the beam diameter
        if self.ss_code == '2' or self.ss_code == '6' or self.ss_code == 'A':
            self.beamDiaComboBox.setCurrentIndex(1)

    def clone_config(self, ss_vm_clone):
        """
        Set the configuration based on the VM given.
        :param ss_vm_clone Clone of the VM.
        :return:
        """
        # Init defaults
        # CWPON
        if ss_vm_clone.cwponCheckBox.isChecked():
            self.cwponCheckBox.setCheckState(2)
            self.cwpon_enable_disable(2)
        else:
            self.cwponCheckBox.setCheckState(0)
            self.cwpon_enable_disable(0)

        # CWPBL
        self.cwpblDoubleSpinBox.setValue(ss_vm_clone.cwpblDoubleSpinBox.value())

        # CWPBN
        self.cwpbnSpinBox.setValue(ss_vm_clone.cwpbnSpinBox.value())

        # CWPBS
        self.cwpbsDoubleSpinBox.setValue(ss_vm_clone.cwpbsDoubleSpinBox.value())

        # CWPBB LL
        self.cwpbbDoubleSpinBox.setValue(ss_vm_clone.cwpbbDoubleSpinBox.value())

        # CWPBB Pulse Type
        self.cwpbbComboBox.setCurrentIndex(ss_vm_clone.cwpbbComboBox.currentIndex())

        # CWPP
        self.cwppSpinBox.setValue(ss_vm_clone.cwppSpinBox.value())

        # CWPTBP
        self.cwptbpDoubleSpinBox.setValue(ss_vm_clone.cwptbpDoubleSpinBox.value())

        # CBTON
        if ss_vm_clone.cbtonCheckBox.isChecked():
            self.cbtonCheckBox.setCheckState(2)
            self.cbton_enable_disable(2)
        else:
            self.cbtonCheckBox.setCheckState(0)
            self.cbton_enable_disable(0)

        # CBTBB
        self.cbtbbComboBox.setCurrentIndex(ss_vm_clone.cbtbbComboBox.currentIndex())

        # CBTTBP
        self.cbttbpDoubleSpinBox.setValue(ss_vm_clone.cbttbpDoubleSpinBox.value())

        # Range Tracking
        self.rangeTrackingComboBox.setCurrentIndex(ss_vm_clone.rangeTrackingComboBox.currentIndex())
        self.cwprt_enable_disable(ss_vm_clone.rangeTrackingComboBox.currentIndex())

        # Range Tracking Fraction
        self.cwprtRangeFractionSpinBox.setValue(ss_vm_clone.cwprtRangeFractionSpinBox.value())

        # Range Tracking Min Bin
        self.cwprtMinBinSpinBox.setValue(ss_vm_clone.cwprtMinBinSpinBox.value())

        # Range Tracking Max Bin
        self.cwprtMaxBinSpinBox.setValue(ss_vm_clone.cwprtMaxBinSpinBox.value())

        # CBI
        if ss_vm_clone.cbiEnabledCheckBox.isChecked():
            self.cbiEnabledCheckBox.setCheckState(2)
            self.cbi_enable_disable(2)
        else:
            self.cbiEnabledCheckBox.setCheckState(0)
            self.cbi_enable_disable(0)

        # CBI Interval
        self.cbiBurstIntervalDoubleSpinBox.setValue(ss_vm_clone.cbiBurstIntervalDoubleSpinBox.value())

        # CBI Num Ens
        self.cbiNumEnsSpinBox.setValue(ss_vm_clone.cbiNumEnsSpinBox.value())

        # CBI Interleaved
        self.cbiInterleaveSpinBox.setValue(ss_vm_clone.cbiInterleaveSpinBox.value())

        # CBI Burst ID
        self.cbiBurstIdSpinBox.setValue(ss_vm_clone.cbiBurstIdSpinBox.value())

        # Num Beams
        self.numBeamsSpinBox.setValue(ss_vm_clone.numBeamsSpinBox.value())

        # Beam Diam
        self.beamDiaComboBox.setCurrentIndex(ss_vm_clone.beamDiaComboBox.currentIndex())

        # Beam Angle
        self.beamAngleComboBox.setCurrentIndex(ss_vm_clone.beamAngleComboBox.currentIndex())

        # CED Beam Vel
        if ss_vm_clone.cedBeamVelCheckBox.isChecked():
            self.cedBeamVelCheckBox.setCheckState(2)
        else:
            self.cedBeamVelCheckBox.setCheckState(0)

        if ss_vm_clone.cedInstrVelCheckBox.isChecked():
            self.cedInstrVelCheckBox.setCheckState(2)
        else:
            self.cedInstrVelCheckBox.setCheckState(0)

        if ss_vm_clone.cedEarthVelCheckBox.isChecked():
            self.cedEarthVelCheckBox.setCheckState(2)
        else:
            self.cedEarthVelCheckBox.setCheckState(0)

        if ss_vm_clone.cedAmpCheckBox.isChecked():
            self.cedAmpCheckBox.setCheckState(2)
        else:
            self.cedAmpCheckBox.setCheckState(0)

        if ss_vm_clone.cedCorrCheckBox.isChecked():
            self.cedCorrCheckBox.setCheckState(2)
        else:
            self.cedCorrCheckBox.setCheckState(0)

        if ss_vm_clone.cedBeamGoodPingCheckBox.isChecked():
            self.cedBeamGoodPingCheckBox.setCheckState(2)
        else:
            self.cedBeamGoodPingCheckBox.setCheckState(0)

        if ss_vm_clone.cedEarthGoodPingCheckBox.isChecked():
            self.cedEarthGoodPingCheckBox.setCheckState(2)
        else:
            self.cedEarthGoodPingCheckBox.setCheckState(0)

        if ss_vm_clone.cedEnsCheckBox.isChecked():
            self.cedEnsCheckBox.setCheckState(2)
        else:
            self.cedEnsCheckBox.setCheckState(0)

        if ss_vm_clone.cedAncCheckBox.isChecked():
            self.cedAncCheckBox.setCheckState(2)
        else:
            self.cedAncCheckBox.setCheckState(0)

        if ss_vm_clone.cedBtCheckBox.isChecked():
            self.cedBtCheckBox.setCheckState(2)
        else:
            self.cedBtCheckBox.setCheckState(0)

        if ss_vm_clone.cedNmeaCheckBox.isChecked():
            self.cedNmeaCheckBox.setCheckState(2)
        else:
            self.cedNmeaCheckBox.setCheckState(0)

        if ss_vm_clone.cedWpEngCheckBox.isChecked():
            self.cedWpEngCheckBox.setCheckState(2)
        else:
            self.cedWpEngCheckBox.setCheckState(0)

        if ss_vm_clone.cedBtEngCheckBox.isChecked():
            self.cedBtEngCheckBox.setCheckState(2)
        else:
            self.cedBtEngCheckBox.setCheckState(0)

        if ss_vm_clone.cedSysSettingCheckBox.isChecked():
            self.cedSysSettingCheckBox.setCheckState(2)
        else:
            self.cedSysSettingCheckBox.setCheckState(0)

        if ss_vm_clone.cedRangeTrackingCheckBox.isChecked():
            self.cedRangeTrackingCheckBox.setCheckState(2)
        else:
            self.cedRangeTrackingCheckBox.setCheckState(0)

        # Disable certain data types if PD0
        if self.predictor.dataFormatComboBox.currentText() == "RTB":
            self.cedWpEngCheckBox.setDisabled(False)
            self.cedBtEngCheckBox.setDisabled(False)
            self.cedSysSettingCheckBox.setDisabled(False)
            self.cedRangeTrackingCheckBox.setDisabled(False)
        else:
            self.cedWpEngCheckBox.setDisabled(True)
            self.cedBtEngCheckBox.setDisabled(True)
            self.cedSysSettingCheckBox.setDisabled(True)
            self.cedRangeTrackingCheckBox.setDisabled(True)

        # Check SS code to know how many beams
        #if self.ss_code == 'A' or self.ss_code == 'B' or self.ss_code == 'C' or self.ss_code == 'D' or self.ss_code == 'E':
        #    self.numBeamsSpinBox.setValue(1)
        #    self.beamAngleComboBox.setCurrentIndex(1)       # 0 Degrees

        # Check the beam diameter
        #if self.ss_code == '2' or self.ss_code == '6' or self.ss_code == 'A':
        #    self.beamDiaComboBox.setCurrentIndex(1)

    def clone_me(self):
        """
        Call parent to clone this configuration.
        :return:
        """
        # Call the parent to clone this configuration
        self.predictor.clone_subsystem(self)

    def init_list(self):
        """
        Initialize all the lists in the VM.
        :return:
        """
        self.cwpbbComboBox.addItem("Broadband", 1)
        self.cwpbbComboBox.addItem("Narrowband", 0)
        self.cwpbbComboBox.addItem("Pulse-Coherent", 4)

        self.cbtbbComboBox.addItem("Broadband", 1)
        self.cbtbbComboBox.addItem("Narrowband", 0)

        self.beamAngleComboBox.addItem("20", 20)
        self.beamAngleComboBox.addItem("0", 0)
        self.beamAngleComboBox.addItem("30", 30)

        self.recommendCfgComboBox.addItem("Default", "Default")
        self.recommendCfgComboBox.addItem("Seafloor Mount", "Seafloor Mount")
        self.recommendCfgComboBox.addItem("Moving Boat", "Moving Boat")
        self.recommendCfgComboBox.addItem("General Purpose [WM1]", "WM1")
        self.recommendCfgComboBox.addItem("Shallow Slow-Moving [WM5]", "WM5")
        self.recommendCfgComboBox.addItem("Shallow [WM8]", "WM8")
        self.recommendCfgComboBox.addItem("Waves", "Waves")
        self.recommendCfgComboBox.addItem("DVL", "DVL")

        self.rangeTrackingComboBox.addItem("Disable", 0)
        self.rangeTrackingComboBox.addItem("Bin", 1)
        self.rangeTrackingComboBox.addItem("Pressure", 2)

        self.beamDiaComboBox.addItem("3 inch", 3)
        self.beamDiaComboBox.addItem("2 inch", 2)
        self.beamDiaComboBox.addItem("1.35 inch", 1.35)
        self.beamDiaComboBox.addItem("1.25 inch", 1.25)
        self.beamDiaComboBox.addItem("5.25 inch", 5.25)

        self.cwprtRangeFractionSpinBox.setEnabled(0)
        self.cwprtMinBinSpinBox.setEnabled(0)
        self.cwprtMaxBinSpinBox.setEnabled(0)

    def closeTab(self):
        """
        Close this tab.
        :return:
        """
        self.predictor.tab_close_requested(self.index)

    def set_tooltips(self):
        """
        Set the tooltip for all the values.  The tooltip will be found
        in a JSON file.  This file can be changed for other languages.
        :return:
        """
        # Get the JSON file
        cmds = JSON.get_json()
        if cmds is None:
            return

        # Set the tooltip
        self.cwponCheckBox.setToolTip(Commands.get_tooltip(cmds["CWPON"]["desc"]))
        self.cwpblDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBL"]["desc"]))
        self.cwpbsDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBS"]["desc"]))
        self.cwpbnSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBN"]["desc"]))
        self.cwpbbDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBB"]["desc"]))
        self.cwpbbComboBox.setToolTip(Commands.get_tooltip(cmds["CWPBB"]["desc"]))
        self.cwppSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPP"]["desc"]))
        self.cwptbpDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPTBP"]["desc"]))
        self.cbtonCheckBox.setToolTip(Commands.get_tooltip(cmds["CBTON"]["desc"]))
        self.cbtbbComboBox.setToolTip(Commands.get_tooltip(cmds["CBTBB"]["desc"]))
        self.cbttbpDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CBTTBP"]["desc"]))
        self.rangeTrackingComboBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cwprtRangeFractionSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cwprtMinBinSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cwprtMaxBinSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cbiEnabledCheckBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiBurstIntervalDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiInterleaveSpinBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiNumEnsSpinBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiBurstIdSpinBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cedGroupBox.setToolTip(Commands.get_tooltip(cmds["CED"]["desc"]))
        self.beamDiaComboBox.setToolTip("Set the Beam diameter.\n2 inches are the smaller beams and 3 inches are the larger beams.")
        self.beamAngleComboBox.setToolTip("Set the Beam angle.  Standard beam angle is 20 degrees.  A vertical beam is 0 degrees.")
        self.predictionGroupBox.setToolTip("Prediction results for the subsystem configuration.")
        self.statusGroupBox.setToolTip("Status of the configuration based off the settings.")
        self.errorGroupBox.setToolTip("Any errors based off the configuration.")
        self.numBeamsGroupBox.setToolTip("Number of beams for the subsystem configuration.\nVertical beam configuration will be 1 beam.")
        self.recommendSettingGroupBox.setToolTip("Select a recommend settings for your deployment.\nThis will load a default setup to begin the configuration.")
        self.cloneButton.setToolTip("Clone this configuration.  A copy of this configuration will be added with the same settings.")

    def stateChanged(self, state):
        """
        Monitor for any state changes then recalculate.
        :param state:
        :return:
        """
        """
        if self.predictor.dataFormatComboBox.currentText() == "PD0":
            self.cedSysSettingCheckBox.setDisabled(True)
            self.cedBtEngCheckBox.setDisabled(True)
            self.cedWpEngCheckBox.setDisabled(True)
            self.cedRangeTrackingCheckBox.setDisabled(True)
        else:
            self.cedSysSettingCheckBox.setDisabled(False)
            self.cedBtEngCheckBox.setDisabled(False)
            self.cedWpEngCheckBox.setDisabled(False)
            self.cedRangeTrackingCheckBox.setDisabled(False)
        """

        # Update the Burst ID
        self.predictor.updateBurstID()

        # Recalculate
        self.predictor.calculate()

    def valueChanged(self, value):
        """
        Monitor for any value changes then recalculate.
        :param state:
        :return:
        """

        # Update the Burst ID
        self.predictor.updateBurstID()

        # Recalculate
        self.predictor.calculate()

    def cwpon_enable_disable(self, state):
        """
        Change the enable state of the values based off
        the selection of CWPON.
        :param state:
        :return:
        """
        enable_state = True
        if state == 2:
            enable_state = True
        else:
            enable_state = False

        self.cwpblDoubleSpinBox.setEnabled(enable_state)
        self.cwpbsDoubleSpinBox.setEnabled(enable_state)
        self.cwpbnSpinBox.setEnabled(enable_state)
        self.cwpbbDoubleSpinBox.setEnabled(enable_state)
        self.cwpbbComboBox.setEnabled(enable_state)
        self.cwppSpinBox.setEnabled(enable_state)
        self.cwptbpDoubleSpinBox.setEnabled(enable_state)

        # Recalculate
        self.predictor.calculate()

    def cbton_enable_disable(self, state):
        """
        Change the enable state of the values based off
        the selection of CBTON.
        :param state:
        :return:
        """
        enable_state = True
        if state == 2:
            enable_state = True
        else:
            enable_state = False

        self.cbtbbComboBox.setEnabled(enable_state)
        self.cbttbpDoubleSpinBox.setEnabled(enable_state)

        # Recalculate
        self.predictor.calculate()

    def cbi_enable_disable(self, state):
        """
        Change the enable state of the values based off
        the selection of Burst Mode.
        :param state:
        :return:
        """
        enable_state = True
        if state == 2:
            enable_state = True
        else:
            enable_state = False

        self.cbiBurstIntervalDoubleSpinBox.setEnabled(enable_state)
        self.cbiNumEnsSpinBox.setEnabled(enable_state)
        self.cbiInterleaveSpinBox.setEnabled(enable_state)
        self.cbiBurstIdSpinBox.setEnabled(enable_state)

        # Update Burst Mode vs Standard Ping Mode
        self.predictor.updateStandardorBurstPinging(enable_state)

        # Recalculate
        self.predictor.calculate()

    def cwprt_enable_disable(self, index):
        """
        Change the enable state of the values based off
        the selection of CWPRT.
        :param index: Current index.
        :return:
        """

        if index == 1:                                                                  # Bin
            self.cwprtRangeFractionSpinBox.setEnabled(0)
            self.cwprtMinBinSpinBox.setEnabled(1)
            self.cwprtMaxBinSpinBox.setEnabled(1)
            if self.cwprtMaxBinSpinBox.value() == 0:                                    # Set a default value
                self.cwprtMaxBinSpinBox.setValue(self.cwpbnSpinBox.value()-1)
        elif index == 2:                                                                # Pressure
            self.cwprtRangeFractionSpinBox.setEnabled(1)
            self.cwprtMinBinSpinBox.setEnabled(0)
            self.cwprtMaxBinSpinBox.setEnabled(0)
        else:                                                                           # Disabled
            self.cwprtRangeFractionSpinBox.setEnabled(0)
            self.cwprtMinBinSpinBox.setEnabled(0)
            self.cwprtMaxBinSpinBox.setEnabled(0)

        # Recalculate
        self.predictor.calculate()

    def calculate(self):
        """
        Calculate the prediction model results based off the settings.
        :return:
        """
        # Get the global settings
        # Get the number of configurations
        num_config = self.predictor.tabSubsystem.count()
        if num_config > 0:
            deployment = self.predictor.deploymentDurationSpinBox.value() / num_config
        else:
            deployment = self.predictor.deploymentDurationSpinBox.value()

        cei = self.predictor.ceiDoubleSpinBox.value()

        # Beam Diameter
        beamDia = 0.075                                 # 3 Inch
        if self.beamDiaComboBox.currentIndex() == 1:
            beamDia = 0.05                              # 2 Inch
        elif self.beamDiaComboBox.currentIndex() == 4:
            beamDia = 0.133                             # 5.25 Inch

        # Calculate
        self.calc_power = Power.calculate_power(DeploymentDuration=deployment,
                                                Beams=self.numBeamsSpinBox.value(),
                                                BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                                CEI=cei,
                                                SystemFrequency=self.freq,
                                                CWPON=self.cwponCheckBox.isChecked(),
                                                CWPBL=self.cwpblDoubleSpinBox.value(),
                                                CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                CWPBN=self.cwpbnSpinBox.value(),
                                                CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                CWPP=self.cwppSpinBox.value(),
                                                CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                CBTON=self.cbtonCheckBox.isChecked(),
                                                CBTBB=self.cbtbbComboBox.itemData(self.cbtbbComboBox.currentIndex()),
                                                BeamDiameter=beamDia,
                                                Salinity=self.predictor.cwsSpinBox.value(),
                                                Temperature=self.predictor.cwtSpinBox.value(),
                                                SpeedOfSound=self.predictor.speedOfSoundSpinBox.value())

        if self.cbiEnabledCheckBox.isChecked():
            self.calc_power = Power.calculate_burst_power(DeploymentDuration=deployment,
                                                          Beams=self.numBeamsSpinBox.value(),
                                                          BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                                          CEI=cei,
                                                          SystemFrequency=self.freq,
                                                          CWPON=self.cwponCheckBox.isChecked(),
                                                          CWPBL=self.cwpblDoubleSpinBox.value(),
                                                          CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                          CWPBN=self.cwpbnSpinBox.value(),
                                                          CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                          CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                          CWPP=self.cwppSpinBox.value(),
                                                          CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                          CBTON=self.cbtonCheckBox.isChecked(),
                                                          CBTBB=self.cbtbbComboBox.itemData(self.cbtbbComboBox.currentIndex()),
                                                          Salinity=self.predictor.cwsSpinBox.value(),
                                                          Temperature=self.predictor.cwtSpinBox.value(),
                                                          SpeedOfSound=self.predictor.speedOfSoundSpinBox.value(),
                                                          CBI=self.cbiEnabledCheckBox.isChecked(),
                                                          CBI_BurstInterval=self.cbiBurstIntervalDoubleSpinBox.value(),
                                                          CBI_NumEns=self.cbiNumEnsSpinBox.value(),
                                                          BeamDiameter=beamDia)
        # Get the battery type
        battery_capacity = self.predictor.batteryTypeComboBox.itemData(self.predictor.batteryTypeComboBox.currentIndex())
        self.calc_num_batt = Power.calculate_number_batteries(DeploymentDuration=deployment,
                                                              PowerUsage=self.calc_power,
                                                              BatteryCapacity=battery_capacity)

        (bt_range, wp_range, first_bin, cfg_range) = Range.calculate_predicted_range(SystemFrequency=self.freq,
                                                                                     Beams=self.numBeamsSpinBox.value(),
                                                                                     BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                                                                     CWPON=self.cwponCheckBox.isChecked(),
                                                                                     CWPBL=self.cwpblDoubleSpinBox.value(),
                                                                                     CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                                                     CWPBN=self.cwpbnSpinBox.value(),
                                                                                     CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                                                     CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                                                     CWPP=self.cwppSpinBox.value(),
                                                                                     CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                                                     CBTON=self.cbtonCheckBox.isChecked(),
                                                                                     BeamDiameter=beamDia,
                                                                                     Salinity=self.predictor.cwsSpinBox.value(),
                                                                                     Temperature=self.predictor.cwtSpinBox.value(),
                                                                                     SpeedOfSound=self.predictor.speedOfSoundSpinBox.value())

        self.calc_bt_range = bt_range
        self.calc_wp_range = wp_range
        self.calc_first_bin = first_bin
        self.calc_cfg_wp_range = cfg_range

        self.calc_max_vel = Velocity.calculate_max_velocity(SystemFrequency=self.freq,
                                                            BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                                            CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                            CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                            CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()))

        if self.cbiEnabledCheckBox.isChecked():
            self.calc_data = DS.calculate_burst_storage_amount(CBI_BurstInterval=self.cbiBurstIntervalDoubleSpinBox.value(),
                                                               CBI_NumEns=self.cbiNumEnsSpinBox.value(),
                                                               DeploymentDuration=deployment,
                                                               Beams=self.numBeamsSpinBox.value(),
                                                               BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                                               CEOUTPUT=self.predictor.dataFormatComboBox.currentText(),
                                                               CEI=cei,
                                                               CWPBN=self.cwpbnSpinBox.value(),
                                                               IsE0000001=self.cedBeamVelCheckBox.isChecked(),
                                                               IsE0000002=self.cedInstrVelCheckBox.isChecked(),
                                                               IsE0000003=self.cedEarthVelCheckBox.isChecked(),
                                                               IsE0000004=self.cedAmpCheckBox.isChecked(),
                                                               IsE0000005=self.cedCorrCheckBox.isChecked(),
                                                               IsE0000006=self.cedBeamGoodPingCheckBox.isChecked(),
                                                               IsE0000007=self.cedEarthGoodPingCheckBox.isChecked(),
                                                               IsE0000008=self.cedEnsCheckBox.isChecked(),
                                                               IsE0000009=self.cedAncCheckBox.isChecked(),
                                                               IsE0000010=self.cedBtCheckBox.isChecked(),
                                                               IsE0000011=self.cedNmeaCheckBox.isChecked(),
                                                               IsE0000012=self.cedWpEngCheckBox.isChecked(),
                                                               IsE0000013=self.cedBtEngCheckBox.isChecked(),
                                                               IsE0000014=self.cedSysSettingCheckBox.isChecked(),
                                                               IsE0000015=self.cedRangeTrackingCheckBox.isChecked(),)
        else:
            self.calc_data = DS.calculate_storage_amount(DeploymentDuration=deployment,
                                                         CEI=cei,
                                                         CEOUTPUT=self.predictor.dataFormatComboBox.currentText(),
                                                         Beams=self.numBeamsSpinBox.value(),
                                                         BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                                         CWPBN=self.cwpbnSpinBox.value(),
                                                         IsE0000001=self.cedBeamVelCheckBox.isChecked(),
                                                         IsE0000002=self.cedInstrVelCheckBox.isChecked(),
                                                         IsE0000003=self.cedEarthVelCheckBox.isChecked(),
                                                         IsE0000004=self.cedAmpCheckBox.isChecked(),
                                                         IsE0000005=self.cedCorrCheckBox.isChecked(),
                                                         IsE0000006=self.cedBeamGoodPingCheckBox.isChecked(),
                                                         IsE0000007=self.cedEarthGoodPingCheckBox.isChecked(),
                                                         IsE0000008=self.cedEnsCheckBox.isChecked(),
                                                         IsE0000009=self.cedAncCheckBox.isChecked(),
                                                         IsE0000010=self.cedBtCheckBox.isChecked(),
                                                         IsE0000011=self.cedNmeaCheckBox.isChecked(),
                                                         IsE0000012=self.cedWpEngCheckBox.isChecked(),
                                                         IsE0000013=self.cedBtEngCheckBox.isChecked(),
                                                         IsE0000014=self.cedSysSettingCheckBox.isChecked(),
                                                         IsE0000015=self.cedRangeTrackingCheckBox.isChecked(),)

        self.calc_ens_size = DS.calculate_ensemble_size(CEOUTPUT=self.predictor.dataFormatComboBox.currentText(),
                                                         CWPBN=self.cwpbnSpinBox.value(),
                                                         Beams=self.numBeamsSpinBox.value(),
                                                         IsE0000001=self.cedBeamVelCheckBox.isChecked(),
                                                         IsE0000002=self.cedInstrVelCheckBox.isChecked(),
                                                         IsE0000003=self.cedEarthVelCheckBox.isChecked(),
                                                         IsE0000004=self.cedAmpCheckBox.isChecked(),
                                                         IsE0000005=self.cedCorrCheckBox.isChecked(),
                                                         IsE0000006=self.cedBeamGoodPingCheckBox.isChecked(),
                                                         IsE0000007=self.cedEarthGoodPingCheckBox.isChecked(),
                                                         IsE0000008=self.cedEnsCheckBox.isChecked(),
                                                         IsE0000009=self.cedAncCheckBox.isChecked(),
                                                         IsE0000010=self.cedBtCheckBox.isChecked(),
                                                         IsE0000011=self.cedNmeaCheckBox.isChecked(),
                                                         IsE0000012=self.cedWpEngCheckBox.isChecked(),
                                                         IsE0000013=self.cedBtEngCheckBox.isChecked(),
                                                         IsE0000014=self.cedSysSettingCheckBox.isChecked(),
                                                         IsE0000015=self.cedRangeTrackingCheckBox.isChecked(),)


        self.calc_std = STD.calculate_std(SystemFrequency=self.freq,
                                          Beams=self.numBeamsSpinBox.value(),
                                          BeamAngle=self.beamAngleComboBox.itemData(self.beamAngleComboBox.currentIndex()),
                                          CWPON=self.cwponCheckBox.isChecked(),
                                          CWPBL=self.cwpblDoubleSpinBox.value(),
                                          CWPBS=self.cwpbsDoubleSpinBox.value(),
                                          CWPBN=self.cwpbnSpinBox.value(),
                                          CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                          CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                          CWPP=self.cwppSpinBox.value(),
                                          CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                          CBTON=self.cbtonCheckBox.isChecked())

        #if self.calc_max_vel is None:
        #    self.calc_max_vel = 0.0
        #if self.calc_std is None:
        #    self.calc_std = 0.0

        # Update the display
        self.powerLabel.setText(str(round(self.calc_power, 2)) + " watt*hr")
        self.numBatteriesLabel.setText(str(round(self.calc_num_batt, 3)) + " batteries")
        self.wpRangeLabel.setText(str(round(self.calc_wp_range, 2)) + " m")
        self.btRangeLabel.setText(str(round(self.calc_bt_range, 2)) + " m")
        self.firstBinPosLabel.setText(str(round(self.calc_first_bin, 2)) + " m")
        self.maxVelLabel.setText(str(round(self.calc_max_vel, 3)) + " m/s")
        self.dataUsageLabel.setText(str(DS.bytes_2_human_readable(self.calc_data)))
        self.stdLabel.setText(str(round(self.calc_std, 3)) + " m/s")

        # Set the ping description
        self.pingingTextBrowser.clear()
        cfg_status_str = ""
        err_status_str = ""

        # CBI
        if self.cbiEnabledCheckBox.isChecked():
            msg, error_msg = Commands.pretty_print_burst(self.predictor.ceiDoubleSpinBox.value(),
                                                         self.cbiBurstIntervalDoubleSpinBox.value(),
                                                         self.cbiNumEnsSpinBox.value(),
                                                         self.cwppSpinBox.value(),
                                                         self.cwptbpDoubleSpinBox.value())
            cfg_status_str += msg
            err_status_str += error_msg
        else:
            msg, error_msg = Commands.pretty_print_standard(self.predictor.ceiDoubleSpinBox.value(),
                                                            self.cwppSpinBox.value(),
                                                            self.cwptbpDoubleSpinBox.value())
            cfg_status_str += msg
            err_status_str += error_msg

        if self.cwponCheckBox.isChecked():
            # Configured Water Profile depth
            msg = Commands.pretty_print_cfg_depth(self.cwpblDoubleSpinBox.value(),
                                                  self.cwpbsDoubleSpinBox.value(),
                                                  self.cwpbnSpinBox.value(),
                                                  self.calc_first_bin)
            cfg_status_str += msg
            err_status_str += error_msg

        # Max Velocity and Accuracy tooltip
        max_vel_acc_tt, error_msg = Commands.pretty_print_accuracy(self.calc_max_vel, self.calc_std)
        err_status_str += error_msg
        self.velAccGroupBox.setToolTip(max_vel_acc_tt)
        self.maxVelLabel.setToolTip(max_vel_acc_tt)
        self.stdLabel.setToolTip(max_vel_acc_tt)
        if self.cwponCheckBox.isChecked():
            cfg_status_str += max_vel_acc_tt

        # Recording turned on
        if self.predictor.cerecordCheckBox.isChecked():
            cfg_status_str += "-Recording to the internal SD card.\n"
        else:
            cfg_status_str += "-Data is NOT recorded internally.\n"

        if self.predictor.dataFormatComboBox.currentText() == "RTB":
            cfg_status_str += "-Data in RTB format.\n"
        else:
            if self.predictor.coordinateTransformComboBox.currentText() == "Beam":
                cfg_status_str += "-Data in PD0 Beam format.\n"
            elif self.predictor.coordinateTransformComboBox.currentText() == "Instrument":
                cfg_status_str += "-Data in PD0 Instrument format.\n"
            elif self.predictor.coordinateTransformComboBox.currentText() == "Earth":
                cfg_status_str += "-Data in PD0 Earth format.\n"
            elif self.predictor.coordinateTransformComboBox.currentText() == "Ship":
                cfg_status_str += "-Data in PD0 Ship format.\n"

        # Ensemble size
        cfg_status_str += '-Ensemble Size: ' + str(DS.bytes_2_human_readable(self.calc_ens_size)) + "\n"

        if self.predictor.cwsSpinBox.value() == 0:
            cfg_status_str += "-Salinity set for FRESH water.\n"
        else:
            cfg_status_str += "-Salinity set for SALT water.\n"

        #cfg_status_str += str(self.calc_max_vel)
        #cfg_status_str += str(self.calc_std)

        # Set the text to the browser
        self.pingingTextBrowser.setText(cfg_status_str)
        self.errorTextBrowser.setText(err_status_str)

    def get_cmd_list(self):
        """
        Create a list of commands.
        :return: List of all the commands with the values.
        """
        command_list = []

        if self.cwponCheckBox.isChecked():
            # CWPON
            if self.cwponCheckBox.isChecked():
                command_list.append(Commands.AdcpCmd("CWPON", "1"))
            else:
                command_list.append(Commands.AdcpCmd("CWPON", "0"))

            # CWPBB
            cwpbb_val = self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex())
            cwpbb_lag = str(self.cwpbbDoubleSpinBox.value())
            command_list.append((Commands.AdcpCmd("CWPBB", str(cwpbb_val) + ", " + cwpbb_lag)))

            command_list.append(Commands.AdcpCmd("CWPBL", str(self.cwpblDoubleSpinBox.value())))        # CWPBL
            command_list.append(Commands.AdcpCmd("CWPBS", str(self.cwpbsDoubleSpinBox.value())))        # CWPBS
            command_list.append(Commands.AdcpCmd("CWPBN", str(self.cwpbnSpinBox.value())))              # CWPBS
            command_list.append(Commands.AdcpCmd("CWPP", str(self.cwppSpinBox.value())))                # CWPP
            command_list.append(Commands.AdcpCmd("CWPTBP", str(self.cwptbpDoubleSpinBox.value())))      # CWPTBP

            # CWPRT
            if self.rangeTrackingComboBox.currentIndex() == 0:
                command_list.append(Commands.AdcpCmd("CWPRT", str(0)))                                  # CWPRT
            elif self.rangeTrackingComboBox.currentIndex() == 1:
                minBin = str(self.cwprtMinBinSpinBox.value())
                maxBin = str(self.cwprtMaxBinSpinBox.value())
                command_list.append(Commands.AdcpCmd("CWPRT", "1, " + minBin + ", " + maxBin))          # CWPRT
            elif self.rangeTrackingComboBox.currentIndex() == 2:
                frac = str(self.cwprtRangeFractionSpinBox.value())
                command_list.append(Commands.AdcpCmd("CWPRT", "2, " + frac))                            # CWPRT

        # CBTON
        if self.cbtonCheckBox.isChecked():
            command_list.append(Commands.AdcpCmd("CBTON", "1"))
        else:
            command_list.append(Commands.AdcpCmd("CBTON", "0"))

        if self.cbtonCheckBox.isChecked():
            #CBTBB
            cbtbb_val = self.cbtbbComboBox.itemData(self.cbtbbComboBox.currentIndex())
            if cbtbb_val == 0:
                command_list.append((Commands.AdcpCmd("CBTBB", "0")))
            else:
                command_list.append((Commands.AdcpCmd("CBTBB", "7")))

            command_list.append(Commands.AdcpCmd("CBTTBP", str(self.cbttbpDoubleSpinBox.value())))      # CBTTBP

        if self.cbiEnabledCheckBox.isChecked():
            cbi_num_ens = str(self.cbiNumEnsSpinBox.value())
            cbi_interval = Commands.sec_to_hmss(self.cbiBurstIntervalDoubleSpinBox.value())
            cbi_interleave = str(self.cbiInterleaveSpinBox.value())
            cbi_burst_id = str(self.cbiBurstIdSpinBox.value())
            command_list.append(Commands.AdcpCmd("CBI", cbi_interval + ", " + cbi_num_ens + " , " + cbi_interleave + ", " + cbi_burst_id))  # CBI

        # CED
        ced = ""
        if self.cedBeamVelCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedInstrVelCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedEarthVelCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedAmpCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedCorrCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedBeamGoodPingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedEarthGoodPingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedEnsCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedAncCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedBtCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedNmeaCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedWpEngCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedBtEngCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedSysSettingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedRangeTrackingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        ced += "00000000000000000"
        command_list.append(Commands.AdcpCmd("CED", ced))               # CED


        return command_list

    def set_preset(self):
        """
        Set the presets from the JSON file.
        :return:
        """
        # Get the JSON file
        json_cmds = JSON.get_json()
        if json_cmds is None:
            return

        if self.recommendCfgComboBox.currentText() == "Default":                                   # Default
            print("Default")
            if self.ss_code == "2":                                                         # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(1)     # 2 inch
            elif self.ss_code == "3":                                                         # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":                                                         # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "General Purpose [WM1]":                                     # WM1
            print("WM1")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "Shallow Slow-Moving [WM5]":  # WM5 and Shallow Slow-Moving
            print("WM5")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "Shallow [WM8]":  # WM8 and Shallow
            print("WM8")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "Seafloor Mount":  # Bottom Mount
            print("Seafloor Mount")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "Waves":  # Waves
            print("Waves")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Waves"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Waves"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Waves"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Waves"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Waves"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Waves"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Waves"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Waves"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Waves"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Waves"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Waves"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "Moving Boat":  # Moving Boat
            print("Moving Boat")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch

        elif self.recommendCfgComboBox.currentText() == "DVL":  # DVL
            print("DVL")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["DVL"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["DVL"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["DVL"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(1)  # 2 inch
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["DVL"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["DVL"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["DVL"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["DVL"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["DVL"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["DVL"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["DVL"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["DVL"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
                self.beamDiaComboBox.setCurrentIndex(0)  # 3 inch


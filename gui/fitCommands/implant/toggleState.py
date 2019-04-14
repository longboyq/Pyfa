import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.implant.toggleState import CalcToggleImplantStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleImplantStateCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Toggle Implant State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position

    def Do(self):
        if self.internalHistory.submit(CalcToggleImplantStateCommand(fitID=self.fitID, position=self.position)):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

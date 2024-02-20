"""
.DESCRIPTION
    Simple Class to log information 
        
.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment_fund_Analyzer
    Creation Date:      20-Feb-2024
    ChangeLog:

    Date            Who                     What

"""
from dataclasses import dataclass
from datetime import datetime

@dataclass()
class Log:
    logFilePath: str
    
    def writeLog(self, type:str, message:str):
        currentTime = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        with open(self.logFilePath, "a") as logFile:
            logFile.write(f"{currentTime} - [Python] - [{type.upper()}] - {message}\n")
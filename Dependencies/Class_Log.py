"""
.DESCRIPTION
    Class to enable logging.
        It allows to log messages even before the log file location will be passed.
        If script fails before setting logs directory, all collected data will be displayed in console.
        
.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      20-Feb-2024
    ChangeLog:

    Date            Who                     What
    2024-03-01      Stanisław Horna         Implemented log cache, cleanUpOldLogFiles, and destructor,
                                            which is printing collected logs to console if they were not saved to file
    
"""
from dataclasses import dataclass, field
from datetime import datetime
import os


@dataclass()
class Log:
    logDir: str = field(init=False, default_factory=str)
    logFilePath: str = field(init=False, default_factory=str)

    logCache: list[str] = field(init=False, default_factory=list)

    def __del__(self) -> None:

        # if log path is not set display logs to the console,
        # as they were not saved to file
        if self.logFilePath == "":
            self.printLogs()

        return None

    def printLogs(self) -> None:
        for log in self.logCache:
            print(log, end="")

        return None

    def setLogDirectory(self, logDirectory: str) -> None:

        # Set provided path as log directory and create log file name for current execution
        self.logDir = logDirectory
        self.logFilePath = os.path.join(
            os.path.abspath(self.logDir),
            datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')
        )

        # try to save collected logs to file
        # if it fails than keep logging to cache to display the logs once deconstructor is called
        try:
            self.emptyLogCache()
            self.writeLog("info", "Cache emptied")
        except:
            self.logFilePath = ""
            self.writeLog("error", "Failed to write collected logs to file")

        return None

    def emptyLogCache(self) -> None:
        
        # Open log file for current execution in append mode
        # loop through all cached logs and save to current log file
        with open(self.logFilePath, "a") as logFile:
            for log in self.logCache:
                logFile.write(log)
                
        return None

    def cleanUpOldLogFiles(self, numberOfLogsToKeep: int) -> None:
        
        
        self.writeLog("info", "Log Directory clean up")
        
        # Get list of files in logs directory and sort ascending by the datetime in the filename
        logFiles = os.listdir(self.logDir)
        dates = sorted(
            datetime.strptime(date.replace(".log", ""), "%Y-%m-%d_%H-%M-%S") for date in logFiles
        )
        
        # loop through dates starting from oldest to newest,
        # iterate until number of remaining files will be same as variable numberOfLogsToKeep
        i = -1
        while (i := i+1) < len(dates) - numberOfLogsToKeep:
            
            # based on sorted dates create absolute log file path
            fileToRemove = os.path.join(
                os.getcwd(),
                self.logDir.replace("./", ""),
                dates[i].strftime('%Y-%m-%d_%H-%M-%S.log')
            )
            
            # try to remove file
            try:
                os.remove(
                    fileToRemove
                )
                self.writeLog("info", f"Log {fileToRemove} removed")
            except:
                self.writeLog("error", f"Failed to remove {fileToRemove}")
        
        return None

    def writeLog(self, type: str, message: str) -> None:
        
        # Get current time and form the log message entry
        currentTime = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        logMessage = f"{currentTime} - [{type.upper()}] - {message}\n"
        
        # If the filePath is set write log directly to the file,
        # otherwise save it in the cache
        if self.logFilePath != "":
            with open(self.logFilePath, "a") as logFile:
                logFile.write(logMessage)
        else:
            self.logCache.append(logMessage)
            
        return None

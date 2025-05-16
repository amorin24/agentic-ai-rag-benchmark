import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface LogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error' | 'success';
  source: string;
  message: string;
  details?: any;
  agentName?: string;
  taskId?: string;
}

interface LogContextType {
  logs: LogEntry[];
  addLog: (log: Omit<LogEntry, 'id' | 'timestamp'>) => void;
  clearLogs: () => void;
  getLogsBySource: (source: string) => LogEntry[];
  getLogsByAgent: (agentName: string) => LogEntry[];
}

const LogContext = createContext<LogContextType | undefined>(undefined);

export const useLogContext = () => {
  const context = useContext(LogContext);
  if (!context) {
    throw new Error('useLogContext must be used within a LogProvider');
  }
  return context;
};

interface LogProviderProps {
  children: ReactNode;
  maxLogs?: number;
}

export const LogProvider: React.FC<LogProviderProps> = ({ 
  children, 
  maxLogs = 1000 
}) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  const addLog = (log: Omit<LogEntry, 'id' | 'timestamp'>) => {
    const newLog: LogEntry = {
      ...log,
      id: `log_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
    };

    setLogs(prevLogs => {
      const updatedLogs = [newLog, ...prevLogs];
      return updatedLogs.slice(0, maxLogs);
    });
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const getLogsBySource = (source: string) => {
    return logs.filter(log => log.source === source);
  };

  const getLogsByAgent = (agentName: string) => {
    return logs.filter(log => log.agentName === agentName);
  };

  useEffect(() => {
    const errorLogs = logs.filter(log => log.level === 'error');
    if (errorLogs.length > 0 && process.env.NODE_ENV === 'development') {
      console.error('Recent error logs:', errorLogs);
    }
  }, [logs]);

  return (
    <LogContext.Provider value={{ 
      logs, 
      addLog, 
      clearLogs, 
      getLogsBySource,
      getLogsByAgent
    }}>
      {children}
    </LogContext.Provider>
  );
};

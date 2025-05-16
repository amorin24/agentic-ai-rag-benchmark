import React, { useState, useEffect } from 'react';
import { useLogContext, LogEntry } from '../contexts/LogContext';

interface LogPanelProps {
  maxHeight?: string;
  filter?: {
    source?: string;
    level?: 'info' | 'warning' | 'error' | 'success';
    agentName?: string;
  };
  autoScroll?: boolean;
  showClearButton?: boolean;
}

const LogPanel: React.FC<LogPanelProps> = ({
  maxHeight = '300px',
  filter,
  autoScroll = true,
  showClearButton = true,
}) => {
  const { logs, clearLogs } = useLogContext();
  const [isExpanded, setIsExpanded] = useState(false);
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'errors' | 'warnings' | 'info'>('all');

  useEffect(() => {
    let filtered = [...logs];
    
    if (filter) {
      if (filter.source) {
        filtered = filtered.filter(log => log.source === filter.source);
      }
      if (filter.level) {
        filtered = filtered.filter(log => log.level === filter.level);
      }
      if (filter.agentName) {
        filtered = filtered.filter(log => log.agentName === filter.agentName);
      }
    }

    if (activeTab === 'errors') {
      filtered = filtered.filter(log => log.level === 'error');
    } else if (activeTab === 'warnings') {
      filtered = filtered.filter(log => log.level === 'warning');
    } else if (activeTab === 'info') {
      filtered = filtered.filter(log => log.level === 'info' || log.level === 'success');
    }

    setFilteredLogs(filtered);
  }, [logs, filter, activeTab]);

  useEffect(() => {
    if (autoScroll && isExpanded) {
      const logContainer = document.getElementById('log-container');
      if (logContainer) {
        logContainer.scrollTop = logContainer.scrollHeight;
      }
    }
  }, [filteredLogs, autoScroll, isExpanded]);

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'text-red-600 bg-red-50';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50';
      case 'success':
        return 'text-green-600 bg-green-50';
      default:
        return 'text-blue-600 bg-blue-50';
    }
  };

  const getLogIcon = (level: string) => {
    switch (level) {
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'success':
        return '✅';
      default:
        return 'ℹ️';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md mb-4">
      <div className="border-b">
        <button
          className="w-full text-left p-3 font-medium flex justify-between items-center bg-gray-50 hover:bg-gray-100 rounded-t-md"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <span className="flex items-center">
            <svg 
              className="w-5 h-5 mr-2" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24" 
              xmlns="http://www.w3.org/2000/svg"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
            System Logs
            <span className="ml-2 px-2 py-1 text-xs bg-gray-200 text-gray-700 rounded">
              {filteredLogs.length}
            </span>
          </span>
          <span>{isExpanded ? '▼' : '►'}</span>
        </button>
      </div>

      {isExpanded && (
        <div>
          <div className="flex border-b">
            <button
              className={`px-4 py-2 font-medium text-sm ${
                activeTab === 'all'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('all')}
            >
              All
            </button>
            <button
              className={`px-4 py-2 font-medium text-sm ${
                activeTab === 'errors'
                  ? 'border-b-2 border-red-500 text-red-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('errors')}
            >
              Errors
            </button>
            <button
              className={`px-4 py-2 font-medium text-sm ${
                activeTab === 'warnings'
                  ? 'border-b-2 border-yellow-500 text-yellow-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('warnings')}
            >
              Warnings
            </button>
            <button
              className={`px-4 py-2 font-medium text-sm ${
                activeTab === 'info'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('info')}
            >
              Info
            </button>
            {showClearButton && (
              <button
                className="ml-auto px-4 py-2 text-sm text-red-500 hover:text-red-700"
                onClick={clearLogs}
              >
                Clear
              </button>
            )}
          </div>

          <div
            id="log-container"
            className="overflow-y-auto p-2"
            style={{ maxHeight }}
          >
            {filteredLogs.length === 0 ? (
              <div className="text-center py-4 text-gray-500">No logs to display</div>
            ) : (
              <div className="space-y-2">
                {filteredLogs.map((log) => (
                  <div
                    key={log.id}
                    className={`p-2 rounded border ${getLevelColor(log.level)}`}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex items-start">
                        <span className="mr-2">{getLogIcon(log.level)}</span>
                        <div>
                          <div className="font-medium">
                            {log.source}
                            {log.agentName && (
                              <span className="ml-2 px-1 py-0.5 text-xs bg-gray-200 text-gray-700 rounded">
                                {log.agentName}
                              </span>
                            )}
                            {log.taskId && (
                              <span className="ml-1 text-xs text-gray-500">
                                #{log.taskId}
                              </span>
                            )}
                          </div>
                          <div className="text-sm">{log.message}</div>
                          {log.details && (
                            <pre className="mt-1 text-xs bg-white p-1 rounded border overflow-x-auto">
                              {typeof log.details === 'string'
                                ? log.details
                                : JSON.stringify(log.details, null, 2)}
                            </pre>
                          )}
                        </div>
                      </div>
                      <div className="text-xs text-gray-500 whitespace-nowrap ml-2">
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default LogPanel;

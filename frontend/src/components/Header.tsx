import React from 'react'
import { useUIStore } from '../store/uiStore'

const Header: React.FC = () => {
  const { sidebarOpen, toggleSidebar } = useUIStore()

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleSidebar}
              className="p-2 rounded-md hover:bg-gray-100"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
            <h1 className="text-xl font-semibold text-gray-900">
              ArchiAI Solution
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">
              AI-Powered Architectural Design
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

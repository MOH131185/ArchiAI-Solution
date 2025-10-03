import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useUIStore } from '../store/uiStore'

const Sidebar: React.FC = () => {
  const { sidebarOpen } = useUIStore()
  const location = useLocation()

  const navigation = [
    { name: 'Home', href: '/', icon: '🏠' },
    { name: 'Projects', href: '/project', icon: '📁' },
    { name: 'Design', href: '/design', icon: '🎨' },
    { name: 'Analysis', href: '/analysis', icon: '📊' },
    { name: 'Export', href: '/export', icon: '📤' },
    { name: 'Cost', href: '/cost', icon: '💰' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ]

  if (!sidebarOpen) return null

  return (
    <aside className="w-64 bg-white shadow-sm border-r h-full">
      <nav className="p-4">
        <ul className="space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <li key={item.name}>
                <Link
                  to={item.href}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar

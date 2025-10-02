import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Helmet } from 'react-helmet'
import { useProjectStore } from './store/projectStore'
import { useUIStore } from './store/uiStore'

// Layout components
import Layout from './components/Layout'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Footer from './components/Footer'

// Page components
import HomePage from './pages/HomePage'
import ProjectPage from './pages/ProjectPage'
import DesignPage from './pages/DesignPage'
import AnalysisPage from './pages/AnalysisPage'
import ExportPage from './pages/ExportPage'
import CostPage from './pages/CostPage'
import SettingsPage from './pages/SettingsPage'
import NotFoundPage from './pages/NotFoundPage'

// Loading components
import LoadingSpinner from './components/LoadingSpinner'
import ErrorBoundary from './components/ErrorBoundary'

function App() {
  const { currentProject } = useProjectStore()
  const { sidebarOpen, theme } = useUIStore()

  return (
    <div className={`min-h-screen bg-background text-foreground ${theme}`}>
      <Helmet>
        <title>ArchiAI Solution - AI-Powered Architectural Design</title>
        <meta name="description" content="AI-powered architectural design system that creates full projects in 2D and 3D with structural and MEP details" />
      </Helmet>
      
      <ErrorBoundary>
        <Layout>
          <Header />
          
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            
            <main className={`flex-1 overflow-auto transition-all duration-300 ${
              sidebarOpen ? 'ml-64' : 'ml-0'
            }`}>
              <div className="container mx-auto px-4 py-6">
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/project" element={<ProjectPage />} />
                  <Route path="/project/:id" element={<ProjectPage />} />
                  <Route path="/design" element={<DesignPage />} />
                  <Route path="/design/:id" element={<DesignPage />} />
                  <Route path="/analysis" element={<AnalysisPage />} />
                  <Route path="/analysis/:id" element={<AnalysisPage />} />
                  <Route path="/export" element={<ExportPage />} />
                  <Route path="/export/:id" element={<ExportPage />} />
                  <Route path="/cost" element={<CostPage />} />
                  <Route path="/cost/:id" element={<CostPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                  <Route path="*" element={<NotFoundPage />} />
                </Routes>
              </div>
            </main>
          </div>
          
          <Footer />
        </Layout>
      </ErrorBoundary>
    </div>
  )
}

export default App

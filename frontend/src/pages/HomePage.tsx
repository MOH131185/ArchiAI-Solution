import React from 'react'

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Welcome to ArchiAI Solution
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            AI-powered architectural design system that creates full projects in 2D and 3D 
            with structural and MEP details, climate-aware design, and cost estimation.
          </p>
          
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">🏗️</div>
              <h3 className="text-xl font-semibold mb-2">AI Design Generation</h3>
              <p className="text-gray-600">
                Generate complete 2D and 3D architectural designs using AI
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">🌍</div>
              <h3 className="text-xl font-semibold mb-2">Climate-Aware Design</h3>
              <p className="text-gray-600">
                Automatically adapt designs to local climate and weather patterns
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-semibold mb-2">Cost Estimation</h3>
              <p className="text-gray-600">
                Generate detailed cost estimates with Excel export
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage

import React from 'react'

const HowItWorks = () => {
  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Page Title */}
        <h1 className="text-white text-3xl font-bold mb-8">How Our AI Works</h1>

        {/* Main Content Card */}
        <div className="bg-slate-800 rounded-lg shadow-lg overflow-hidden max-w-3xl mx-auto">
          <div className="p-8 md:p-12 prose prose-invert prose-lg max-w-none">
            
            {/* Section 1: Our Mission */}
            <section>
              <h2 className="text-white text-2xl font-bold mb-4">Our Mission</h2>
              <p className="text-gray-300 leading-relaxed">
                Our mission is to democratize access to financial information. We use state-of-the-art 
                AI to scan, analyze, and simplify complex market news, providing you with clear, actionable 
                insights in real-time.
              </p>
            </section>

            {/* Section 2: Our Technology */}
            <section className="mt-10">
              <h2 className="text-white text-2xl font-bold mb-6">Our 3-Step Process</h2>
              
              <div className="mt-8 space-y-10">
                
                {/* Step 1: Scan */}
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      fill="none" 
                      viewBox="0 0 24 24" 
                      strokeWidth="2" 
                      stroke="currentColor" 
                      className="w-6 h-6 text-indigo-400"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-white text-xl font-bold mb-2">1. Scan</h3>
                    <p className="text-gray-300 leading-relaxed">
                      Our system constantly monitors dozens of top-tier Indian financial news sources, 
                      blogs, and press releases 24/7, ensuring you never miss a critical update.
                    </p>
                  </div>
                </div>

                {/* Step 2: Analyze */}
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      fill="none" 
                      viewBox="0 0 24 24" 
                      strokeWidth="2" 
                      stroke="currentColor" 
                      className="w-6 h-6 text-indigo-400"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-white text-xl font-bold mb-2">2. Analyze</h3>
                    <p className="text-gray-300 leading-relaxed">
                      An advanced AI model reads every article, understands the context, extracts key topics, 
                      and determines the overall sentiment (Positive, Negative, or Neutral) and its potential 
                      market impact.
                    </p>
                  </div>
                </div>

                {/* Step 3: Deliver */}
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      fill="none" 
                      viewBox="0 0 24 24" 
                      strokeWidth="2" 
                      stroke="currentColor" 
                      className="w-6 h-6 text-indigo-400"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-white text-xl font-bold mb-2">3. Deliver</h3>
                    <p className="text-gray-300 leading-relaxed">
                      We filter out the noise and present this analysis to you in a clean, easy-to-understand 
                      format through our dashboard, news feeds, and personalized watchlists.
                    </p>
                  </div>
                </div>

              </div>
            </section>

            {/* Section 3: Important Disclaimer */}
            <section className="mt-10">
              <h2 className="text-white text-2xl font-bold mb-4">Important Disclaimer</h2>
              
              <div className="mt-6 not-prose bg-yellow-800/20 border-l-4 border-yellow-500 rounded-r-md p-6">
                <p className="font-bold text-yellow-300">
                  This is not financial advice.
                </p>
                <p className="text-yellow-200 mt-2 leading-relaxed">
                  All information and AI-generated analysis on this website are for informational and 
                  educational purposes only. They do not constitute financial, investment, or trading advice. 
                  Always conduct your own research and consult with a qualified financial advisor before making 
                  any investment decisions.
                </p>
              </div>
            </section>

          </div>
        </div>
      </div>
    </div>
  )
}

export default HowItWorks

import React, { useState } from 'react'

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    category: '',
    message: ''
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Form submitted:', formData)
    // Reset form after submission
    setFormData({
      name: '',
      email: '',
      category: '',
      message: ''
    })
    alert('Thank you for your feedback! We will get back to you soon.')
  }

  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Page Title */}
        <h1 className="text-white text-3xl font-bold mb-8">Contact & Feedback</h1>

        {/* Main Content Card */}
        <div className="bg-slate-800 rounded-lg shadow-lg overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2">
            
            {/* Section 1: Text Content */}
            <div className="p-8 md:p-12">
              <h2 className="text-white text-2xl font-bold mb-4">We Value Your Feedback</h2>
              
              <p className="text-lg text-gray-300 leading-relaxed">
                Whether you've found a bug, have a feature request, or want to report an AI misclassification, 
                we want to hear from you.
              </p>
              
              <p className="mt-4 text-gray-400 leading-relaxed">
                Your feedback is crucial for improving our platform's accuracy and usefulness. Please use the 
                form to send us your thoughts.
              </p>

              <p className="mt-8 text-gray-400 leading-relaxed">
                For all other inquiries, you can reach our team directly at:
              </p>
              
              <a 
                href="mailto:contact@aimarketinsights.demo" 
                className="block text-indigo-400 font-medium hover:text-indigo-300 mt-2 transition-colors"
              >
                contact@aimarketinsights.demo
              </a>
            </div>

            {/* Section 2: Feedback Form */}
            <div className="p-8 md:p-12 border-t border-slate-700 md:border-t-0 md:border-l">
              <form action="#" method="POST" onSubmit={handleSubmit} className="space-y-6">
                
                {/* Name Field */}
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full mt-1 px-3 py-2 bg-slate-700 text-white border border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                  />
                </div>

                {/* Email Field */}
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full mt-1 px-3 py-2 bg-slate-700 text-white border border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                  />
                </div>

                {/* Category Field */}
                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-gray-300 mb-1">
                    Feedback Category
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    required
                    className="w-full mt-1 px-3 py-2 bg-slate-700 text-white border border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none cursor-pointer transition"
                  >
                    <option value="">Select a category...</option>
                    <option value="General Inquiry">General Inquiry</option>
                    <option value="Bug Report">Bug Report</option>
                    <option value="Feature Request">Feature Request</option>
                    <option value="AI Misclassification">AI Misclassification</option>
                  </select>
                </div>

                {/* Message Field */}
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-300 mb-1">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows="5"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    placeholder="Please describe your feedback..."
                    className="w-full mt-1 px-3 py-2 bg-slate-700 text-white border border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-y"
                  ></textarea>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  className="w-full py-3 px-4 bg-indigo-600 text-white font-semibold rounded-md shadow-md hover:bg-indigo-500 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-slate-800"
                >
                  Submit Feedback
                </button>

              </form>
            </div>

          </div>
        </div>
      </div>
    </div>
  )
}

export default Contact

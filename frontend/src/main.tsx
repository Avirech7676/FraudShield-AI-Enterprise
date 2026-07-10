import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ClerkProvider } from '@clerk/react'
import './index.css'
import App from './App.tsx'

const clerkPublishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY
const hasClerkKey = clerkPublishableKey?.startsWith('pk_')

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {hasClerkKey ? (
      <ClerkProvider publishableKey={clerkPublishableKey}>
        <App />
      </ClerkProvider>
    ) : (
      <main className="login-page">
        <section className="login-panel">
          <div className="brand-mark">FS</div>
          <h1>Clerk key required</h1>
          <p>Add VITE_CLERK_PUBLISHABLE_KEY to frontend/.env and restart Vite.</p>
        </section>
      </main>
    )}
  </StrictMode>,
)

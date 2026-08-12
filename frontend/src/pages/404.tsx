const Error404Page = () => {
  return (
    <div className="error-page">
      <div className="error-content">
        <div className="error-code">404</div>
        <h1>Page Not Found</h1>
        <p>
          The page you're looking for doesn't exist or has been moved.
        </p>
        <div className="error-actions">
          <a href="/" className="btn btn-primary">
            Go to Home
          </a>
          <a href="/dashboard" className="btn btn-secondary">
            Go to Dashboard
          </a>
        </div>
      </div>
    </div>
  );
};

export default Error404Page;
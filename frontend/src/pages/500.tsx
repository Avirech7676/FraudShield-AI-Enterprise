const Error500Page = () => {
  return (
    <div className="error-page">
      <div className="error-content">
        <div className="error-code">500</div>
        <h1>Internal Server Error</h1>
        <p>
          Something went wrong on our end. Please try again later or contact
          support if the issue persists.
        </p>
        <div className="error-actions">
          <a href="/" className="btn btn-primary">
            Go to Home
          </a>
          <button
            onClick={() => window.location.reload()}
            className="btn btn-secondary"
          >
            Refresh Page
          </button>
        </div>
      </div>
    </div>
  );
};

export default Error500Page;
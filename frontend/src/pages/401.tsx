const Error401Page = () => {
  return (
    <div className="error-page">
      <div className="error-content">
        <div className="error-code">401</div>
        <h1>Unauthorized</h1>
        <p>
          You are not authorized to access this page. Please log in with the
          appropriate credentials.
        </p>
        <div className="error-actions">
          <a href="/login" className="btn btn-primary">
            Go to Login
          </a>
          <a href="/" className="btn btn-secondary">
            Go to Home
          </a>
        </div>
      </div>
    </div>
  );
};

export default Error401Page;
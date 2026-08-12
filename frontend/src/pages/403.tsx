const Error403Page = () => {
  return (
    <div className="error-page">
      <div className="error-content">
        <div className="error-code">403</div>
        <h1>Forbidden</h1>
        <p>
          You don't have permission to access this resource. Please contact your
          administrator if you believe this is a mistake.
        </p>
        <div className="error-actions">
          <a href="/dashboard" className="btn btn-primary">
            Go to Dashboard
          </a>
          <a href="/" className="btn btn-secondary">
            Go to Home
          </a>
        </div>
      </div>
    </div>
  );
};

export default Error403Page;
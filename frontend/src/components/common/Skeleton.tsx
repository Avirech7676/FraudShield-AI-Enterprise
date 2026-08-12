const SkeletonText = ({ width = "100%", height = "1rem", className = "" }) => {
  return (
    <div
      className={`skeleton-text ${className}`}
      style={{ width, height, borderRadius: "4px" }}
    />
  );
};

const SkeletonCircle = ({ size = "2rem", className = "" }) => {
  return (
    <div
      className={`skeleton-circle ${className}`}
      style={{ width: size, height: size, borderRadius: "50%" }}
    />
  );
};

const SkeletonRect = ({ width = "100%", height = "1rem", className = "" }) => {
  return (
    <div
      className={`skeleton-rect ${className}`}
      style={{ width, height, borderRadius: "4px" }}
    />
  );
};

const SkeletonCard = ({ titleLines = 3, contentLines = 5, className = "" }) => {
  return (
    <div className={`skeleton-card ${className}`}>
      <div className="skeleton-header">
        {[...Array(titleLines)].map((_, index) => (
          <SkeletonText
            key={index}
            width={index === 0 ? "60%" : "80%"}
            height="0.875rem"
            className="mb-1"
          />
        ))}
      </div>
      <div className="skeleton-body">
        {[...Array(contentLines)].map((_, index) => (
          <SkeletonText key={index} width="100%" height="0.75rem" className="mb-1" />
        ))}
      </div>
    </div>
  );
};

const SkeletonTable = ({ rows = 3, className = "" }) => {
  return (
    <div className={`skeleton-table ${className}`}>
      <table>
        <thead>
          <tr>
            {[...Array(4)].map((_, _colIndex) => (
              <th key={_colIndex}>
                <SkeletonText width="100%" height="1rem" />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {[...Array(rows)].map((_rowIndex, i) => (
            <tr key={i}>
              {[...Array(4)].map((_colIndex, j) => (
                <td key={j}>
                  <SkeletonText width="100%" height="0.875rem" />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const Skeleton = ({ height = 120, ...props }) => {
  return <div className="skeleton" style={{ height }} {...props} />;
};

export {
  Skeleton,
  SkeletonText,
  SkeletonCircle,
  SkeletonRect,
  SkeletonCard,
  SkeletonTable,
};

export default Skeleton;
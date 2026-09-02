type Props = {
  page: number;
  pages: number;
  setPage: (page: number) => void;
};

export default function HistoryPagination({ page, pages, setPage }: Props) {
  if (pages <= 1) return null;

  const items: React.ReactNode[] = [];

  items.push(
    <button key="prev" className="page-btn" disabled={page === 1} onClick={() => setPage(page - 1)}>
      ←
    </button>
  );

  const start = Math.max(1, page - 2);
  const end = Math.min(pages, page + 2);

  if (start > 1) {
    items.push(
      <button key={1} className="page-btn" onClick={() => setPage(1)}>1</button>
    );
    if (start > 2) {
      items.push(<span key="dots1" style={{ color: "var(--text-faint)", padding: "0 4px" }}>···</span>);
    }
  }

  for (let i = start; i <= end; i++) {
    items.push(
      <button key={i} className={`page-btn ${i === page ? "active" : ""}`} onClick={() => setPage(i)}>
        {i}
      </button>
    );
  }

  if (end < pages) {
    if (end < pages - 1) {
      items.push(<span key="dots2" style={{ color: "var(--text-faint)", padding: "0 4px" }}>···</span>);
    }
    items.push(
      <button key={pages} className="page-btn" onClick={() => setPage(pages)}>{pages}</button>
    );
  }

  items.push(
    <button key="next" className="page-btn" disabled={page === pages} onClick={() => setPage(page + 1)}>
      →
    </button>
  );

  return <div className="pagination"><div className="pages">{items}</div></div>;
}
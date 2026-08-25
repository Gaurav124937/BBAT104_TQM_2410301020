from database.connection import get_connection

def search_records(query="", status="All"):
    query=query.strip()
    sql="""
    SELECT i.issue_id,b.title AS book_title,m.name AS member_name,
           i.issue_date,i.due_date,
           CASE WHEN i.returned=1 THEN 'Returned'
                WHEN DATE(i.due_date)<DATE('now') THEN 'Overdue'
                ELSE 'Active' END AS status,
           r.return_id,r.return_date
    FROM issues i
    JOIN books b ON b.book_id=i.book_id
    JOIN members m ON m.member_id=i.member_id
    LEFT JOIN returns r ON r.issue_id=i.issue_id
    WHERE 1=1
    """
    params=[]
    if query:
        like=f"%{query}%"
        sql += """ AND (b.title LIKE ? OR m.name LIKE ?
                    OR CAST(i.issue_id AS TEXT) LIKE ?
                    OR CAST(r.return_id AS TEXT) LIKE ?)"""
        params=[like,like,like,like]
    if status=="Active":
        sql+=" AND i.returned=0"
    elif status=="Returned":
        sql+=" AND i.returned=1"
    elif status=="Overdue":
        sql+=" AND i.returned=0 AND DATE(i.due_date)<DATE('now')"
    sql+=" ORDER BY DATE(i.issue_date) DESC,i.issue_id DESC"
    with get_connection() as c:
        return c.execute(sql,params).fetchall()

def get_record_summary():
    with get_connection() as c:
        r=c.execute("""
        SELECT COUNT(*) total,
               SUM(CASE WHEN returned=0 THEN 1 ELSE 0 END) active,
               SUM(CASE WHEN returned=0 AND DATE(due_date)<DATE('now') THEN 1 ELSE 0 END) overdue,
               SUM(CASE WHEN returned=1 THEN 1 ELSE 0 END) returned
        FROM issues
        """).fetchone()
    return {k:int(r[k] or 0) for k in ("total","active","overdue","returned")}

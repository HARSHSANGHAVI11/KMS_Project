import psycopg2
import openai
from datetime import datetime

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="company_portal",
        user="postgres",
        password="satnam@61",
        port="5432"
    )


# Fetch recent incidents
def get_recent_incidents(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT project_name, description, date
        FROM incident_logs
        ORDER BY date DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    incidents = []
    for row in rows:
        incidents.append({
            "project": row[0],          # project_name
            "incident_text": row[1],    # description
            "created_at": row[2]        # date
        })
    return incidents


# Generate blog from incidents
def generate_blog_from_incidents(incidents):
    if not incidents:
        return "No incidents available for blog generation."

    incident_summary = "\n".join(
        [f"- [{i['created_at']}] {i['project']}: {i['incident_text']}"
         for i in incidents]
    )

    prompt = f"""
    You are an AI knowledge blogger.
    Write a blog article from the following incidents in a professional but simple style.
    
    Incidents:
    {incident_summary}

    Blog:
    """

    # Here we assume you use Ollama (local model) instead of OpenAI
    import subprocess, json
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

def run_blog_agent():
    incidents = get_recent_incidents(limit=10)
    blog = generate_blog_from_incidents(incidents)

    # Save blog into DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO blogs (title, content, created_at)
        VALUES (%s, %s, %s)
    """, ("Auto-generated Blog", blog, datetime.now()))
    conn.commit()
    conn.close()

    print("✅ Blog Generated:\n")
    print(blog)

if __name__ == "__main__":
    run_blog_agent()

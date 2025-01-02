import time

import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_html
from typing import Dict, Any
import json
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, Response

app = Flask(__name__)


# Sample DataFrames
df1 = pd.DataFrame({
    "Column1": [1, 2, 3],
    "Column2": ["A", "B", "C"]
})

df2 = pd.DataFrame({
    "Column1": [4, 5, 6],
    "Column2": ["D", "E", "F"]
})

# Sample Plotly Chart
fig = go.Figure(data=[go.Bar(x=["A", "B", "C"], y=[1, 3, 2])])


def format_output(input_content: Any) -> str:
    """
    Formats and returns output in HTML format.

    Args:
        input_content (Any): The content to format and display.

    Returns:
        str: Formatted HTML string.
    """
    html_content = ""

    if isinstance(input_content, pd.DataFrame):
        # Convert DataFrame to HTML table
        html_content = input_content.to_html(index=False, classes="table table-striped", border=0)

    elif isinstance(input_content, go.Figure):
        # Convert Plotly chart to HTML
        html_content = to_html(input_content, full_html=False, include_plotlyjs='cdn')

    elif isinstance(input_content, str):
        specific_string_type = "markdown"

        # Check if the string is HTML
        try:
            soup = BeautifulSoup(input_content, "html.parser")
            if bool(soup.find()):
                specific_string_type = "html"
        except (TypeError, UnicodeDecodeError):
            pass

        # Check if the string is JSON
        try:
            json.loads(input_content)
            specific_string_type = "json"
        except ValueError:
            pass

        if specific_string_type == "html":
            html_content = input_content
        elif specific_string_type == "json":
            html_content = f"<pre>{json.dumps(json.loads(input_content), indent=2)}</pre>"
        else:
            html_content = f"<p>{input_content}</p>"

    else:
        html_content = f"<p>{str(input_content)}</p>"

    return html_content


def stream_last_node(state: dict) -> None:
    """
    Handles interaction and generates HTML output based on the state.

    Args:
        state (Dict[str, Any]): The current state of the planning agent.

    Returns:
        dict: JSON containing the HTML content.
    """
    html_content = ''

    for key in state:
        # Display Main Answer
        if key == "answer":
            html_content += f"<div class='section'><h2>Main Response</h2>{format_output(state['answer'])}</div>"

        # Handle PCAP Errors
        if state == "pcap_error_analysis":
            html_content += "<div class='section'><h2>PCAP Error Analysis</h2>"
            for item in state["pcap_error_analysis"]:
                for element in item:
                    html_content += format_output(element)
            html_content += "</div>"

        # Handle SIP Errors
        if key == "sip_call_flow_error_analysis":
            html_content += "<div class='section'><h2>SIP Call Flow Error Analysis</h2>"
            for item in state["sip_call_flow_error_analysis"]:
                html_content += format_output(f"**SIP call ID**: {item.get('sip_call_id', 'N/A')}")
                html_content += format_output(f"**Analysis**: {item.get('analysis', 'No analysis provided.')}")
                html_content += format_output(item.get('dataframe', df1))
            html_content += "</div>"

        # Handle HTTP2 Errors
        if key == "http2_call_flow_error_analysis":
            html_content += "<div class='section'><h2>HTTP2 Call Flow Error Analysis</h2>"
            for item in state["http2_call_flow_error_analysis"]:
                html_content += format_output(f"**HTTP2 Stream ID**: {item.get('http2_streamid', 'N/A')}")
                html_content += format_output(f"**Analysis**: {item.get('analysis', 'No analysis provided.')}")
                html_content += format_output(item.get('dataframe', df1))
            html_content += "</div>"

        # Handle Other Protocol Errors
        if key == "all_protocol_error_analysis_except_sip_and_http2":
            html_content += "<div class='section'><h2>Other Protocol Errors</h2>"
            for item in state["all_protocol_error_analysis_except_sip_and_http2"]:
                html_content += format_output(f"**Protocol**: {item.get('protocol', 'Unknown')}")
                html_content += format_output(f"**Analysis**: {item.get('analysis', 'No analysis provided.')}")
                html_content += format_output(item.get('dataframe', df2))
            html_content += "</div>"

        # Handle Solution Results
        if key == "solution_results":
            html_content += "<div class='section'><h2>Solution Results</h2>"
            for step, solution in state["solution_results"].items():
                html_content += f"<h3>{step}</h3>"
                for report in solution.get("analysis_report", []):
                    html_content += format_output(report)
                for error in solution.get("error_report", []):
                    html_content += format_output(error)
                for sql_result in solution.get("sql_results", []):
                    html_content += format_output(sql_result)
                if "chart" in solution and solution["chart"]:
                    html_content += format_output(fig)
            html_content += "</div>"

        chunk = json.dumps({'value': html_content})
        yield f"data: {chunk}\n\n"
        time.sleep(1)


@app.post('/')
def get_response():
    return Response(stream_last_node(test_input), mimetype='text/event-stream')


def check_credentials(username: str, password: str) -> bool:
    USERNAME = 'admin'
    PASSWORD = 'admin'
    return username == USERNAME and password == PASSWORD


@app.post('/login')
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    if check_credentials(username, password):
        return jsonify({ "msg": "OK"}), 200
    return jsonify({ "msg": "Bad username or password"}), 401


#Test Input
test_input = {
    "answer": "Here is the primary response to your question.",
    "pcap_error_analysis": [
        ["PCAP Error 1: Invalid header detected.", "PCAP Error 2: Packet loss identified."]
    ],
    "sip_call_flow_error_analysis": [
        {
            "sip_call_id": "SIP12345",
            "analysis": "Timeout detected during SIP call setup.",
            "dataframe": df1
        },
        {
            "sip_call_id": "SIP67890",
            "analysis": "Authentication failure detected.",
            "dataframe": df2
        }
    ],
    "http2_call_flow_error_analysis": [
        {
            "http2_streamid": "HTTP2_STREAM_001",
            "analysis": "Connection reset error observed.",
            "dataframe": df1
        }
    ],
    "all_protocol_error_analysis_except_sip_and_http2": [
        {
            "protocol": "FTP",
            "analysis": "Transfer failed due to incomplete handshake.",
            "dataframe": df2
        }
    ],
    "solution_results": {
        "step1": {
            "analysis_report": [
                "Step 1: Data validation passed successfully.",
                "Step 1: No anomalies detected in the process."
            ],
            "error_report": [
                "Step 1: Minor configuration mismatch.",
                "Step 1: Logging incomplete in certain cases."
            ],
            "sql_results": [
                df1,
                df2
            ],
            "chart": fig
        },
        "step2": {
            "analysis_report": [
                "Step 2: Data aggregation completed.",
                "Step 2: Results matched expected benchmarks."
            ],
            "error_report": [
                "Step 2: Timeout during aggregation step."
            ],
            "sql_results": [
                df2
            ]
        }
    },
    "documents": [
        "Document 1: Architecture Guide.pdf",
        "Document 2: Debug Logs.txt"
    ],
    "low_confidence": False,
    "is_hallucination": False,
    "solution_steps": {
        "step1": "Extract and validate raw data.",
        "step2": "Aggregate and analyze data.",
        "step3": "Generate final reports."
    },
    "conversation_history": [
        {"role": "user", "content": "What is the status of SIP calls?"},
        {"role": "assistant", "content": "Investigating SIP call flows..."}
    ],
    "internet_search_results": [
        "Search Result 1: Troubleshooting SIP errors.",
        "Search Result 2: Common SIP timeout scenarios."
    ],
    "current_table_name": "error_logs",
    "current_schema_name": "production",
    "analysis_report": [
        "Global analysis completed without critical errors.",
        "All validation checks passed successfully."
    ],
    "error_report": [
        "Global Warning: Configuration inconsistency detected.",
        "Minor issue in data indexing."
    ],
    "generation_finished": True
}

# Sample Input State
state = {
    "answer": "Here is the primary response to your question.",
    "sip_call_flow_error_analysis": [{"sip_call_id": "SIP12345", "analysis": "Timeout detected.", "dataframe": df1}],
    "solution_results": {"step1": {"chart": fig}}
}

if __name__ == "__main__":
    app.run(debug=True, port=8000)

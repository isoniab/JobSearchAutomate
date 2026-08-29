import http.server
import socketserver
import json
import os
import urllib.parse
import sys
import time

DIRECTORY = "/Users/tarun/Desktop/JobSearchAutomate"
sys.path.append(DIRECTORY)

from add_company import add_company
from main import run_job_search_automation
from engine.pdf_converter import PDFConverter

PORT = 8085

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?', 1)[0].split('#', 1)[0]
        path = urllib.parse.unquote(path)
        if path == "/" or path == "/index.html":
            return os.path.join(DIRECTORY, "web", "index.html")
        elif path == "/api/jobs":
            return os.path.join(DIRECTORY, "data", "latest_matches.json")
        elif path == "/api/config":
            return os.path.join(DIRECTORY, "config.json")
        return super().translate_path(path)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        
        if parsed_url.path == "/api/jobs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data_file = os.path.join(DIRECTORY, "data", "latest_matches.json")
            if os.path.exists(data_file):
                with open(data_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"{}")
            return

        elif parsed_url.path == "/api/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            config_file = os.path.join(DIRECTORY, "config.json")
            if os.path.exists(config_file):
                with open(config_file, "rb") as f:
                    self.wfile.write(f.read())
            return

        elif parsed_url.path == "/api/get-resume":
            query_params = urllib.parse.parse_qs(parsed_url.query)
            comp = query_params.get("company", [""])[0]
            title = query_params.get("title", [""])[0]

            res_dir = os.path.join(DIRECTORY, "tailored_resumes")
            md_files = [f for f in os.listdir(res_dir) if f.endswith(".md")]

            target_md = None
            for f in md_files:
                if comp.lower() in f.lower() or title.lower() in f.lower():
                    target_md = f
                    break

            if target_md:
                full_md_path = os.path.join(res_dir, target_md)
                with open(full_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "filename": target_md,
                    "content": content
                }).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
            return

        elif parsed_url.path.startswith("/tailored_resumes/"):
            rel_path = urllib.parse.unquote(parsed_url.path[len("/tailored_resumes/"):])
            rel_path = rel_path.split('?', 1)[0]
            res_dir = os.path.join(DIRECTORY, "tailored_resumes")
            
            exact_path = os.path.join(res_dir, rel_path)
            
            if os.path.exists(exact_path):
                full_path = exact_path
            else:
                pdf_files = [f for f in os.listdir(res_dir) if f.endswith(".pdf")]
                target_file = None
                for f in pdf_files:
                    if rel_path.lower() in f.lower() or f.lower() in rel_path.lower():
                        target_file = f
                        break
                full_path = os.path.join(res_dir, target_file) if target_file else None

            if full_path and os.path.exists(full_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(full_path)}"')
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.send_header("Content-Length", str(os.path.getsize(full_path)))
                self.end_headers()
                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/add-company":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            comp_name = data.get("name")
            career_url = data.get("url")

            if comp_name:
                add_company(comp_name, career_url)
                run_job_search_automation()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": f"Added {comp_name} and triggered scan!"}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
            return

        elif self.path == "/api/save-resume":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            filename = data.get("filename")
            content = data.get("content")

            if filename and content:
                res_dir = os.path.join(DIRECTORY, "tailored_resumes")
                md_path = os.path.join(res_dir, filename)
                pdf_filename = filename.replace(".md", ".pdf")
                pdf_path = os.path.join(res_dir, pdf_filename)

                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(content)

                # Recompile PDF
                PDFConverter().convert_markdown_to_pdf(md_path, pdf_path)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Resume saved & PDF recompiled successfully!",
                    "pdf_filename": pdf_filename,
                    "pdf_url": f"/tailored_resumes/{pdf_filename}?t={int(time.time())}"
                }).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
            return

        elif self.path == "/api/run-scan":
            run_job_search_automation()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Manual scan triggered!"}).encode('utf-8'))
            return

def start_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), DashboardHandler) as httpd:
        print(f"🚀 JobSearchAutomate Web Dashboard running at: http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()

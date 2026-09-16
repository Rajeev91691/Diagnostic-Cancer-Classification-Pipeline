import time
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_live_demo():
    print("=" * 70)
    print("  CONNECTING TO CHROME DEBUG SESSION (PORT 9222)")
    print("=" * 70)
    
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Open a dedicated demo tab
    driver.execute_script("window.open('');")
    demo_handle = driver.window_handles[-1]
    driver.switch_to.window(demo_handle)
    
    base_dir = r"C:\Users\rajee\Desktop\ml-intern-assignment"
    html_path = os.path.join(base_dir, "results", "notebook_presentation.html")
    file_url = "file:///" + urllib.parse.quote(html_path.replace("\\", "/"), safe=":/")
    
    print(f"\n[1/6] Navigating to Notebook Presentation: {file_url}")
    driver.get(file_url)
    time.sleep(3)
    
    # Smooth scroll through key stages of the project
    print("[2/6] Demonstrating Problem Statement, Dataset & EDA Sections...")
    driver.execute_script("window.scrollTo({top: 600, behavior: 'smooth'});")
    time.sleep(2.5)
    
    driver.execute_script("window.scrollTo({top: 1400, behavior: 'smooth'});")
    time.sleep(2.5)
    
    print("[3/6] Demonstrating Visualizations (Distributions & Correlation Heatmap)...")
    driver.execute_script("window.scrollTo({top: 2400, behavior: 'smooth'});")
    time.sleep(3)
    
    driver.execute_script("window.scrollTo({top: 3200, behavior: 'smooth'});")
    time.sleep(3)
    
    print("[4/6] Demonstrating Preprocessing, Model Training & Evaluation Metrics...")
    driver.execute_script("window.scrollTo({top: 4200, behavior: 'smooth'});")
    time.sleep(3)
    
    print("[5/6] Demonstrating Confusion Matrix (98.25% Acc) & Feature Importance...")
    driver.execute_script("window.scrollTo({top: 5200, behavior: 'smooth'});")
    time.sleep(3)
    
    driver.execute_script("window.scrollTo({top: 6200, behavior: 'smooth'});")
    time.sleep(3)
    
    print("[6/6] Demonstrating Live Model Serialization & Inference Demonstration...")
    driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
    time.sleep(4)
    
    # Also open the 3-Page PDF Report in a second tab
    pdf_path = os.path.join(base_dir, "report", "Internship_Assignment_Report.pdf")
    pdf_url = "file:///" + urllib.parse.quote(pdf_path.replace("\\", "/"), safe=":/")
    print(f"\n[DEMO] Opening 3-Page Executive PDF Report: {pdf_url}")
    driver.execute_script(f"window.open('{pdf_url}', '_blank');")
    time.sleep(3)
    
    print("\n" + "=" * 70)
    print("  LIVE CHROME DEMO COMPLETED SUCCESSFULLY")
    print("  Interactive Notebook and 3-Page Report are live in your Chrome window.")
    print("=" * 70)

if __name__ == "__main__":
    run_live_demo()

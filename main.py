import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

def crawl_data(apartment_name):
    # Selenium 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # GUI 없이 실행
    service = Service()  # chromedriver가 PATH에 있다고 가정
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://land.naver.com"
    driver.get(url)
    time.sleep(1)

    # 검색 입력 및 실행
    search_box = driver.find_element(By.ID, 'queryInputHeader')
    search_box.send_keys(apartment_name)
    search_box.submit()
    time.sleep(2)

    # 결과 수집
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, '.item_inner')
    for item in items[:10]:
        try:
            title = item.find_element(By.CSS_SELECTOR, '.item_title').text
            price = item.find_element(By.CSS_SELECTOR, '.price').text
            detail = item.find_element(By.CSS_SELECTOR, '.info_area').text
            results.append({'제목': title, '가격': price, '세부정보': detail})
        except:
            continue

    driver.quit()
    return results

def export_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def run_crawler():
    apt_name = entry.get()
    if not apt_name:
        messagebox.showwarning("경고", "아파트명을 입력하세요.")
        return

    messagebox.showinfo("알림", f"'{apt_name}' 매물 정보를 수집합니다. 잠시만 기다려 주세요.")
    data = crawl_data(apt_name)
    if not data:
        messagebox.showwarning("결과 없음", "매물 정보를 찾을 수 없습니다.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        export_to_excel(data, save_path)
        messagebox.showinfo("완료", "엑셀 파일로 저장되었습니다.")

# GUI 구성
root = tk.Tk()
root.title("네이버 부동산 매물 크롤러")

tk.Label(root, text="아파트명 입력:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="크롤링 시작", command=run_crawler).pack(pady=10)

root.mainloop()

# Rideshare Regional Demand Ranking Model
# 叫車區域需求排序模型

[English Version](#english-version) | [中文版](#中文版)

---

## English Version

### Project Overview
Instead of predicting taxi fares using regression, this project predicts Regional Demand through a Ranking methodology. By identifying high-demand regions ahead of time, fleet managers can optimize vehicle positioning and efficiency.

### Model Performance
Using the `YetiRank` loss function, the model achieved an **NDCG@3 score of 0.8433**. This indicates the model can accurately identify the true "Top 3" regions for real-time fleet dispatching.

### ETL Pipeline Architecture
* **Extract**: Data sourced from the Kaggle Boston Uber and Lyft dataset.
* **Transform**: Aggregated via pandas `groupby` to calculate actual ride demand for different regions within the same timeframe, transforming raw data into structured features (weather, time, weekend status).
* **Load**: Processed data is fed into a CatBoost Ranker model. CatBoost natively handles categorical features like region names (`source`) and utilizes symmetric trees to prevent overfitting.

### SHAP Analysis and Commercial Insights

**I. SHAP Chart Interpretation Baseline**
* **Color**: Red indicates high feature values; blue indicates low values.
* **X-axis (Impact)**: Positive values (right) indicate increased demand; negative values (left) indicate decreased demand. Distance from 0 reflects the magnitude of impact.

**II. Feature Importance Overview**
The model relies on "Location" and "Weekend Status" for fundamental data partitioning. For absolute predicted values, "Location" and "Time" cause the most significant fluctuations, while weather factors act as secondary adjustment variables.

**III. Core Features Analysis**

* **Location (source) & Time (hour)**
These are the primary drivers of demand. Their distribution is wide and evenly scattered across positive and negative ranges, indicating a non-linear relationship. The model relies heavily on their interaction to calculate overall demand.

* **Rain Intensity (precipIntensity)**
Light or no rain has minimal impact. However, heavy rain shows a significant negative impact on demand. This suggests that during extreme weather, overall demand decreases as people cancel outdoor activities.

* **Temperature (temperature)**
Both high and low temperatures scatter across both sides of 0. Extreme temperatures do not unilaterally increase or decrease demand; their impact depends on the specific time and location context.

* **Weekend Status (is_weekend)**
Weekdays (low values) show stable baseline support for the market. Weekends (high values) are more dispersed, occasionally falling into the negative range, indicating that weekend demand can sometimes drop below weekday levels depending on other conditions.

### Visualizing the Interactions
1. **Interactive Heatmap (`plot/demand_heatmap.html`)**: Displays demand clusters across 24 hours and 12 regions, showing distinct peaks (e.g., 8 AM/5 PM for business districts, late night for entertainment areas).
2. **Interactive Spatial Map (`plot/boston_demand_map.html`)**: Maps the 12 regions using Folium, categorized by urban function, providing geographical context for the ranking model's predictions.

---

## 中文版

### 專案概述
有別於多數專測計程車資的分析，本專案預測「地區需求 (Regional Demand)」。透過將問題轉化為排序 (Ranking) 任務，預測同時段內各地區的相對熱門順序，藉此協助車隊進行事前調度。

### 模型表現
本模型搭配 `YetiRank` 損失函數，取得 **0.8433 的 NDCG@3 分數**，能有效且精準地辨識出前三名的叫車熱區，提供實務調度參考。

### ETL 資料管線架構
* **Extract (萃取)**：使用 Kaggle 波士頓 Uber 與 Lyft 開源資料集。
* **Transform (轉換)**：使用 pandas 的 `groupby` 功能，統計同一時間段內不同地區的實際叫車需求量，將訂單轉換為包含天氣、時間等特徵的結構化資料。
* **Load (載入)**：將資料載入 CatBoost 排序模型。CatBoost 可直接處理字串型態的地區名稱 (`source`)，並透過對稱樹 (Symmetric Trees) 結構降低過度擬合風險。

### SHAP 圖表解析與商業洞察

**一、 SHAP 圖表判讀基準**
* **顏色**：紅色代表原始數值較高；藍色代表數值較低。
* **橫軸 (影響力)**：落於 0 右側表示增加需求；左側表示減少需求。距離 0 越遠，影響幅度越大。

**二、 特徵重要性總覽**
模型建立決策樹時，依賴「地點」與「週末狀態」進行基礎劃分。在推動數值波動上，「地點」與「時間」造成最廣泛的影響，天氣因素則為次要的動態調整變數。

**三、 核心特徵分析**

* **地點 (source) 與 時間 (hour)**
此二者為影響預測數值的核心變數，其高低數值廣泛散佈於正負區間，具備複雜的非線性影響。模型高度依賴這兩者的交互作用來精確計算總體需求。

* **降雨強度 (precipIntensity)**
無雨或微雨狀態對預測幾乎無影響。高降雨強度則有顯著比例落在負向區間，顯示極端雨勢可能導致民眾取消外出，使總體叫車需求萎縮。

* **溫度 (temperature)**
高溫與低溫皆散佈在 0 的兩側。極端溫度對需求的增減不具絕對的單一方向性，需視當時的時間與地點條件共同判定。

* **週末狀態 (is_weekend)**
代表平日的低數值集中在 0 附近且微幅偏右，顯示平日通勤提供穩定的需求支撐。代表週末的高數值分佈較發散，且部分落在負值區間，顯示特定條件下，週末總需求可能低於平日。

### 資料視覺化
1. **互動式熱力圖 (`plot/demand_heatmap.html`)**：將 24 小時與 12 個地區的平均叫車量繪製成熱力圖。可觀察到商業區尖峰落在早晚通勤時段，而夜生活區尖峰落在深夜，反映時間因子的影響。
2. **波士頓互動式地圖 (`plot/boston_demand_map.html`)**：透過 Folium 將地區以真實經緯度標示於地圖上，並依都市樣貌分類，為排序模型的預測提供地理脈絡。

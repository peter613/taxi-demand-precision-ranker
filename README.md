# Rideshare Regional Demand Ranking Model
# 叫車區域需求排序模型

[English Version](#english-version) | [中文版](#中文版)

---

## English Version

### Project Overview
While most business analytics projects in the rideshare industry focus on predicting taxi fares or prices using regression, this project takes a different approach: Predicting Regional Demand using a Ranking methodology. By understanding where the demand will be highest, fleet managers and drivers can optimize their positioning ahead of time, maximizing efficiency and precision.

### Model Performance
By defining this as a ranking problem and using `YetiRank`, the model achieved an **NDCG@3 score of 0.8433**. This high precision means the model can successfully and accurately identify the true "Top 3 Hottest Regions" for dispatching, providing immense value for real-time fleet management.

### ETL Pipeline Architecture
This project is structured around a standard ETL (Extract, Transform, Load) data pipeline:

* **Extract (E)**: The raw data is extracted from the Kaggle Boston Uber and Lyft dataset (Source: https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma?resource=download).
* **Transform (T)**: Using pandas `groupby`, the data is aggregated to calculate the total ride demand (order_count) for different regions at the exact same time. This process extracts the contextual features (temperature, precipitation, hour, weekend status) and transforms absolute ride counts into relative demand profiles for the ranking model.
* **Load (L)**: The transformed data is loaded into the CatBoost Ranker model. Unlike traditional Random Forest models, CatBoost natively handles string categorical variables, allowing the region's text name (`source`) to be used directly as a feature. Furthermore, CatBoost utilizes symmetric trees, which makes it less prone to overfitting and highly efficient for this ranking task.

### SHAP Analysis and Commercial Insights
To ensure objectivity and consistency in interpretation, this analysis relies on the following visual logic of SHAP (SHapley Additive exPlanations):

**I. SHAP Chart Interpretation Baseline**
* **Feature Value (Color):** Represents the magnitude of the raw data. Red indicates high values (e.g., heavy rain, high temperature, late-night hours); blue indicates low values (e.g., no rain, low temperature, early-morning hours).
* **Impact Direction and Magnitude (X-axis):** Represents the feature's influence on the predicted target (taxi demand).
  * Data points on the right of 0 (positive values) indicate the condition increases demand.
  * Data points on the left of 0 (negative values) indicate the condition decreases demand.
  * The further away from 0, the greater the magnitude of impact on the prediction.

**II. Feature Importance Overview**
Combining the underlying tree model's (CatBoost) feature importance with the SHAP impact distribution, the prediction logic of this model operates on two levels:
* **Model Structural Foundation:** When building decision tree paths, the model heavily relies on "Location (`source`)" and "Weekend Status (`is_weekend`)" for fundamental data partitioning, which is crucial for reducing overall prediction error.
* **Primary Drivers of Numerical Fluctuation:** In terms of pushing the absolute predicted values up or down, "Location (`source`)" and "Time (`hour`)" cause the most extensive and profound fluctuations. Weather factors (temperature and rain) act as secondary, dynamic adjustment variables.

**III. Core Features and Commercial Insights**
Based on the SHAP distribution, the objective impact of each variable on overall demand is as follows:

**Interaction between Location (`source`) and Time (`hour`)**
These are the most central variables affecting predictions. High and low values (red and blue dots) for these features are broadly and evenly scattered across both positive and negative ranges. This shows that time and location have significant, complex, non-linear effects on demand—no single variable can determine the outcome. The model heavily relies on their interaction (e.g., specific times at specific locations) to accurately calculate total demand.

**Rain Intensity (`precipIntensity`) [Crucial Insight & Simpson's Paradox]**
The chart shows that most no-rain or light-rain conditions (blue dots) have almost no impact on predictions. Notably, high rain intensity (red dots) has a significant portion falling on the left side (negative impact). This shatters the intuitive assumption that "rain inevitably increases taxi demand." because people cancel their outdoor plans entirely.

**Temperature (`temperature`)**
High temperatures (red dots) and low temperatures (blue dots) are both scattered on both sides of 0. This further validates the non-linear interactive nature of the model: extreme temperatures do not absolutely drive impact in a single direction. Whether they increase or decrease demand depends on the combination of time and location conditions at that moment.

**Weekend Status (`is_weekend`)**
Low values representing weekdays (blue dots) are highly concentrated near 0 and lean slightly right, showing that weekday commuting patterns provide a stable baseline support for the taxi market. High values representing weekends (red dots) are more scattered, with some falling into the negative range, indicating that under certain conditions, overall weekend demand can actually drop below weekday levels.

### Visualizing the Interactions
To empirically prove the crossover interactions found in the SHAP analysis, three visual tools were generated:
1. **Interactive Heatmap (`plot/demand_heatmap.html`)**: Plotting 24 hours against the 12 regions reveals distinct demand clusters. Business districts (e.g., Financial District) clearly peak at 8 AM and 5 PM, while nightlife areas (e.g., Theatre District) peak late at night. This perfectly visualizes the dual-sided nature of the `hour` feature.
2. **Interactive Spatial Map (`plot/boston_demand_map.html`)**: The 12 regions are plotted on a map using Folium, color-coded by urban function. This geographical context makes the ranking model's behaviors completely interpretable.

---

## 中文版

### 專案概述
目前多數的叫車服務商業分析，通常將目標設定在「預測計程車車資」，並使用傳統的迴歸分析。本專案採取了截然不同的視角：預測「地區需求 (Regional Demand)」。透過將問題轉化為排序 (Ranking) 任務，本專案專注於預測同一個時段內各地區的相對熱門順序，這能大幅且精確地提高預測準確度，完美揪出叫車熱區。

### 模型表現 (Model Performance)
透過將商業問題轉化為嚴謹的排序任務，並搭配 `YetiRank` 損失函數，本模型在預測各時段的熱門地區時，取得了**0.8433 的 NDCG@3分數**！這代表當系統向車隊推薦「Top 3 叫車熱區」時，具備了極高的排序精準度，能直接轉換為實質的調度收益。

### ETL 資料管線架構
本專案的程式碼設計採用了標準的 ETL (Extract, Transform, Load) 流程：

* **Extract (萃取)**：採用 Kaggle 提供的波士頓 Uber 與 Lyft 開源資料集。
* **Transform (轉換)**：使用 pandas 的 `groupby` 功能，統計「同一時間 (group_id)」下「不同地區 (source)」的實際叫車需求量 (demand)。此步驟將原始的訂單資料，轉換成可用於機器學習的特徵矩陣（包含溫度、降水、時間與週末狀態），並匯出成乾淨的結構化檔案。
* **Load (載入)**：將清理好的資料載入 CatBoost 排序模型中進行訓練。有別於傳統的 Random Forest 模型，CatBoost 可以直接讀取字串型態的資料，因此可以直接將「地區名稱 (source)」作為特徵輸入。此外，CatBoost 的底層採用了「對稱樹 (Symmetric Trees)」結構，不僅能有效防止過度擬合，還能大幅提升排序預測的穩定性與效果。

### SHAP 圖表解析與商業洞察

**一、 SHAP 圖表判讀基準**
為確保解讀的客觀性與一致性，本分析基於以下 SHAP (SHapley Additive exPlanations) 視覺化邏輯進行推論：
* **特徵數值 (顏色)**：圖中顏色代表原始資料的數值高低。紅色代表數值較高（如：大雨、高溫、晚間時段）；藍色代表數值較低（如：無雨、低溫、凌晨時段）。
* **影響方向與幅度 (橫軸)**：橫軸代表該特徵對預測目標（計程車需求）的影響力。
  * 資料點落於 0 的右側 (正值)，表示該條件會增加需求。
  * 資料點落於 0 的左側 (負值)，表示該條件會減少需求。
  * 距離中心點 0 越遠，代表該條件對預測結果的影響幅度越大。

**二、 特徵重要性總覽**
綜合底層樹狀模型（CatBoost）的特徵重要性與 SHAP 影響力分佈，本模型的預測邏輯可分為兩個層級：
* **模型結構分類基礎**：模型在建立決策樹路徑時，高度依賴「地點 (source)」與「是否為週末 (is_weekend)」進行基礎資料劃分，這對降低整體預測誤差至關重要。
* **數值波動主要驅動力**：在實際推動需求增減的絕對數值上，「地點 (source)」與「時間 (hour)」造成了最廣泛且深遠的波動。相對而言，天氣因素（溫度與降雨）屬於次要的動態調整變數。

**三、 核心特徵與商業洞察分析**
依據 SHAP 圖表分佈特徵，各變數對總體需求的客觀影響如下：

**地點 (source) 與 時間 (hour) 的交互作用**
此二者為影響預測數值的最核心變數。圖表中這兩個特徵的高低數值（紅藍點）廣泛且均勻地散佈在正值與負值區間。這顯示時間與地點對需求具有顯著且複雜的非線性影響，單一變數無法決定全局。模型高度依賴這兩者的交互作用（例如特定時間搭配特定地點）來精確計算總體需求。

**降雨強度 (precipIntensity) [關鍵反直覺洞察與辛普森悖論]**
圖表顯示，多數無雨或微雨（藍點）狀態對預測幾乎無影響。值得注意的是，高降雨強度（紅點）不僅出現在正值區間，更有顯著比例落在左側（負向影響）。這打破了「下雨必定增加叫車需求」的直覺。
因為當雨勢達到極端情況時，人們傾向直接取消外出行程，總體活動人數的驟降導致總體叫車需求隨之萎縮。

**溫度 (temperature)**
高溫（紅點）與低溫（藍點）皆散佈在 0 的兩側。這進一步印證了非線性模型的交互作用特性：極端溫度並不絕對帶來單一方向的影響。其對需求的增減，需視當時的時間與地點條件共同判定。

**是否為週末 (is_weekend)**
代表平日的低數值（藍點）高度集中在 0 的附近且微幅偏向右側，顯示平日通勤規律為計程車市場提供了穩定的基礎需求支撐。代表週末的高數值（紅點）分佈較為發散，且有部分落在負值區間，顯示在特定條件下，週末的總體需求量反而會低於平日水準。

### 資料視覺化：驗證交叉效應
為了用實際數據證明 SHAP 所發現的現象，本專案提供了三份視覺化圖表：
1. **互動式熱力圖 (`plot/demand_heatmap.html`)**：將 24 小時與 12 個地區的平均叫車量繪製成熱力圖。圖表中可以極度清晰地看到，商業區的叫車尖峰精準落在早上 8 點與下午 5 點；而夜生活區的尖峰則落在深夜。這完美解釋了時間因子 (`hour`) 在 SHAP 圖中為何會呈現廣泛分佈的現象。
2. **波士頓互動式地圖 (`plot/boston_demand_map.html`)**：透過 Folium 將這 12 個地區以真實經緯度打在互動地圖上，並依據都市樣貌進行顏色分類。這份地理脈絡讓 Ranker 模型的一切推測變得具備高度的說服力與可解釋性。

import matplotlib.pyplot as plt
import numpy as np
from sklift.metrics import uplift_by_percentile
from sklift.metrics import qini_curve, perfect_qini_curve 
from sklift.metrics import uplift_curve, perfect_uplift_curve


def custom_uplift_by_percentile(y_true, uplift, treatment, 
                               kind='line', bins=10, string_percentiles=True, 
                               figsize=(10, 6), title=None):
    """
    Построение графика uplift по перцентилям.
    
    Аргументы:
        y_true: Бинарные целевые значения
        uplift: Прогнозируемые значения uplift
        treatment: Бинарные индикаторы воздействия
        kind: 'line' или 'bar'
        bins: Количество перцентильных корзин
        string_percentiles: Отображать ли перцентили в виде строк
        figsize: Размер рисунка (кортеж)
        title: Пользовательский заголовок для графика
    
    Возвращает:
        Рисунок matplotlib
    """
    
    # получаем данные по перцентилям, используя функцию из sklift
    df = uplift_by_percentile(
        y_true, uplift, treatment, strategy='overall',
        std=True, total=False, bins=bins, string_percentiles=False
    )
    
    # извлекаем перцентили из индекса DataFrame
    percentiles = df.index[:bins].values.astype(float)
    
    # извлекаем значения отклика для тестовой группы и их стандартные отклонения
    response_rate_trmnt = df.loc[percentiles, 'response_rate_treatment'].values
    std_trmnt = df.loc[percentiles, 'std_treatment'].values
    
    # извлекаем значения отклика для контрольной группы и их стандартные отклонения
    response_rate_ctrl = df.loc[percentiles, 'response_rate_control'].values
    std_ctrl = df.loc[percentiles, 'std_control'].values
    
    # извлекаем значения uplift и их стандартные отклонения
    uplift_score = df.loc[percentiles, 'uplift'].values
    std_uplift = df.loc[percentiles, 'std_uplift'].values
    
    # создаём график
    fig, ax = plt.subplots(figsize=figsize)
    
    if kind == 'line':
        # строим линейный график для тестовой группы с погрешностями
        ax.errorbar(
            percentiles, response_rate_trmnt, yerr=std_trmnt,
            linewidth=2, color='forestgreen', label='Отклик тестовой группы'
        )
        # строим линейный график для контрольной группы с погрешностями
        ax.errorbar(
            percentiles, response_rate_ctrl, yerr=std_ctrl,
            linewidth=2, color='orange', label='Отклик контрольной группы'
        )
        # строим линейный график для uplift с погрешностями
        ax.errorbar(
            percentiles, uplift_score, yerr=std_uplift,
            linewidth=2, color='red', label='Uplift'
        )
        # заполняем область между линиями тестовой и контрольной групп
        ax.fill_between(percentiles, response_rate_trmnt,
                        response_rate_ctrl, alpha=0.1, color='red')
        
        # добавляем горизонтальную линию на уровне 0, если есть отрицательные значения uplift
        if np.amin(uplift_score) < 0:
            ax.axhline(y=0, color='black', linewidth=1)
            
    elif kind == 'bar':
        # вычисляем ширину столбцов для столбчатой диаграммы
        width = percentiles[1] - percentiles[0] if len(percentiles) > 1 else 5
        bar_width = width * 0.35
        
        # строим столбцы для тестовой, контрольной групп и для uplift
        ax.bar(percentiles - bar_width, response_rate_trmnt, bar_width, 
               color='forestgreen', label='Отклик тестовой группы')
        ax.bar(percentiles, response_rate_ctrl, bar_width, 
               color='orange', label='Отклик контрольной группы')
        ax.bar(percentiles + bar_width, uplift_score, bar_width, 
               color='red', label='Uplift')
    
    # устанавливаем метки по оси X
    if string_percentiles:
        # создаём строковые метки для перцентилей (диапазоны)
        percentiles_str = [f"0-{percentiles[0]:.0f}"] + \
                          [f"{percentiles[i]:.0f}-{percentiles[i + 1]:.0f}" 
                           for i in range(len(percentiles) - 1)]
        ax.set_xticks(percentiles)
        ax.set_xticklabels(percentiles_str, rotation=45)
    else:
        # используем числовые значения перцентилей
        ax.set_xticks(percentiles)
    
    # устанавливаем подписи осей и заголовок
    ax.set_xlabel('Перцентиль')
    ax.set_ylabel('Уровень отклика / Uplift')
    
    # устанавливаем заголовок, если он предоставлен
    if title:
        ax.set_title(title)
  
    # добавляем легенду и сетку для улучшения читаемости
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # оптимизируем расположение элементов на графике
    plt.tight_layout()
    return fig

def plot_qini_curve(y_true, pred_uplift, treat_true):
    res_model = qini_curve(y_true, pred_uplift, treat_true)
    res_perfect = perfect_qini_curve(y_true, treat_true) # Идеальная модель

    # 2. Строим график через обычный matplotlib
    plt.figure(figsize=(7, 5))

    # Кривая нашей модели
    plt.plot(res_model[0], res_model[1], label='Learner', color='blue', lw=2)

    # Кривая идеального выбора
    plt.plot(res_perfect[0], res_perfect[1], label='Perfect Model', color='green', lw=2)

    # Кривая случайного выбора (Random Baseline)
    plt.plot([0, res_model[0][-1]], [0, res_model[1][-1]], label='Random Baseline', color='orange', lw=1)

    plt.title('Qini Curve (sklift metrics)')
    plt.xlabel('Number of targeted customers')
    plt.ylabel('Cumulative Number of Incremental Outcomes')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

def plot_uplift_curve(y_true, pred_uplift, treat_true):
    curve_model = uplift_curve(y_true, pred_uplift, treat_true)
    curve_perfect = perfect_uplift_curve(y_true, treat_true)

    # 2. Строим график вручную
    plt.figure(figsize=(7, 5))

    # Кривая вашей модели
    plt.plot(curve_model[0], curve_model[1], label='Learner', color='blue', lw=2)

    # Кривая идеального выбора (Perfect)
    plt.plot(curve_perfect[0], curve_perfect[1], label='Perfect Model', color='green', lw=2)

    # Кривая случайного выбора (Random Baseline)
    plt.plot([0, curve_model[0][-1]], [0, curve_model[1][-1]], label='Random Baseline', color='orange', lw=1)

    plt.title('Uplift Curve (sklift metrics)')
    plt.xlabel('Number of targeted customers')
    plt.ylabel('Cumulative Incremental Outcome')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

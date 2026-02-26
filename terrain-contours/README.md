# Terrain Contour Generator 🗺️

Построение горизонталей (изолиний рельефа) из облака точек с экспортом в DXF.

## Пайплайн

1. Чтение CSV (X, Y, Z)
2. Триангуляция Делоне (TIN) — `scipy.spatial.Delaunay`
3. Генерация изолиний — `matplotlib.tri` + `contour`
4. Экспорт в DXF — `ezdxf` (LWPOLYLINE + подписи высот)
5. Визуализация PNG — цветная карта с горизонталями

## Установка

```bash
pip3 install scipy matplotlib ezdxf numpy
```

## Использование

```bash
python3 terrain_to_dxf.py --input points.csv --output result.dxf --step 1.0 --png preview.png
```

### Параметры

| Параметр | По умолчанию | Описание |
|----------|-------------|----------|
| `--input` | *(обязательный)* | CSV файл с точками (X, Y, Z) |
| `--output` | `output.dxf` | Выходной DXF |
| `--step` | `1.0` | Шаг горизонталей, м |
| `--png` | `preview.png` | PNG визуализация |

### Формат CSV

```csv
X,Y,Z
100.00,200.00,125.30
...
```

## Демо

```bash
python3 generate_demo.py                    # 500 точек холмистого рельефа
python3 terrain_to_dxf.py --input demo_points.csv --output demo.dxf --step 2.0 --png demo_preview.png
```

## Результат демо

- **500** точек, **982** треугольника TIN
- **23** уровня, **66** изолиний (шаг 2м)
- **132** DXF-объекта (полилинии + подписи)

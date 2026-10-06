# Qué he hecho y qué no

Se ha completado todo el código requerido en `common_code.cpp`, pasando con éxito todos los tests unitarios (6/6):

- `fsiv_convert_image_byte_to_float`: Ok
- `fsiv_convert_image_float_to_byte`: Ok
- `convert_image_bgr_to_hsv`: Ok
- `convert_image_hsv_to_bgr`: Ok
- `fsiv_cbg_process` (only_luma == false): Ok
- `fsiv_cbg_process` (BGR, only_luma == true): Ok

No queda ninguna parte pendiente por implementar.

# Enlace al vídeo describiendo la práctica

[https://youtu.be/Oe-64wje2mg]

Capítulos:
```
00:00 Introducción: Objetivo y formulación I' = c * I^g + b
00:54 Parámetro b (Brillo y desplazamiento lineal)
01:47 Parámetro c (Contraste y rango dinámico)
02:37 Parámetro g (Gamma y respuesta no lineal)
03:54 Parámetro l (Solo Luma: Comparativa BGR vs HSV)
```

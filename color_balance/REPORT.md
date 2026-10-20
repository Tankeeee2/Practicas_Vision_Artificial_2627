# Qué he hecho y qué no

Se ha completado todo el código requerido en `common_code.cpp`, pasando con éxito todos los tests unitarios (6/6):

- `fsiv_color_rescaling`: Ok
- `fsiv_convert_bgr_to_gray`: Ok
- `fsiv_gray_world_color_balance`: Ok
- `fsiv_compute_image_histogram`: Ok
- `fsiv_compute_histogram_percentile` (`p_value=0.0`, `1.0` y `0.79`): Ok
- `fsiv_white_patch_color_balance` (`p=0` y `0.13`): Ok

No queda ninguna parte pendiente por implementar.

# Enlace al vídeo describiendo la práctica

[https://youtu.be/mpnNMWJBNhM]

Capítulos:
```
00:00 Introducción
00:45 Parámetro p
```
*(Desglose de la demostración del parámetro p: 00:45 White Patch clásico p=0, 01:39 White Patch robusto p=10, 02:12 valores altos de p, 02:39 Gray World p=100).*

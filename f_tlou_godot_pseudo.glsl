shader_type spatial;

uniform vec3 n; //normal del plano
uniform float h; //distancia desde el origen al plano a lo largo de n

void fragment() {
    vec3 p = (CAMERA_MATRIX * vec4(VERTEX, 1)).xyz; //posicion pixel-mundo
    float x = dot(p, n) - h;
    ALBEDO = vec3(1, 0, 0); //rojo, vec3 ALBEDO = vec3(1, 0, 0);

    if (x < 0) {
        ALBEDO = vec3(0, 1, 0); //verde
    }
}

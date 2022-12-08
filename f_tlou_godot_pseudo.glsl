shader_type spatial;

uniform vec3 n; //normal del plano
uniform float h; //distancia desde el origen al plano a lo largo de n

void fragment() {
    vec4 world_pos = CAMERA_MATRIX * vec4(VERTEX, 1);
    float dist = world_pos.y * sharpness;
    dist = clamp(dist + 1.0 / 2, 0, 1);
    ALBEDO = mix(ColourA, ColourB, dist).xyz;
}

'''void fragment() {
    vec3 p = (CAMERA_MATRIX * vec4(VERTEX, 1)).xyz; //posicion pixel-mundo
    float x = dot(p, n) - h;
    ALBEDO = vec3(1, 0, 0); //rojo, vec3 ALBEDO = vec3(1, 0, 0);

    if (x < 0) {
        ALBEDO = vec3(0, 1, 0); //verde
    }
}'''

#version 330 core
out vec4 fragColor; //color para cada fragmento

uniform vec2 u_resolution;
uniform float u_time;

float map(vec3 p) { //sdf esfera
    return length(p) - 3.0 / 5;
}

float rayMarch(vec3 ro, vec3 rd) {
    float dist = 0;

    for (int i = 0; i < 256; i++) {
        vec3 p = dist * rd + ro; //vector p
        float hit = map(p); //distancia mas corta al obj
        dist += hit;

        if (dist > 100 || abs(hit) < 1e-4) i = 256; //rompe bucle cuando esta lo suf cerca del obj o cuando el rayo escapa de la escena
    }

    return dist;
}

vec3 render() { //color basado en la posicion del pixel en la pantalla
    vec2 uv = (2 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y; //centra el origen de la pantalla
    vec3 col = vec3(0); //inicia negro

    vec3 ro = vec3(0, 0, -1), rd = normalize(vec3(uv, 1)); //origen_Rayo, dir_Rayo
    float dist = rayMarch(ro, rd); //dist al obj

    if (dist < 100) {
        col += dist; //suma la distancia al color resultante
    }

    return col;
}

void main() {
    vec3 color = render(); 

    fragColor = vec4(color, 1);
}

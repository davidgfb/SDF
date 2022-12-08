#version 460
in vec3 in_position; //vertices pantalla

void main() {
    gl_Position = vec4(in_position, 1); //rasteriza pantalla en fragmentos, vertices --> fragmentos
}

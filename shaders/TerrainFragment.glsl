#version 330 core

in vec3 v_Normal;
in vec4 v_FragPos;
in float v_Visibility;

out vec4 o_Color;

uniform vec3 u_SunPos;
uniform float u_Noise;

void main()
{
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(vec3(0, -1, 0));
    float diff = max(dot(norm, lightDir), 0.0) * 5;
    vec3 diffuse = (diff + 2) * vec3(1.0, 1.0, 1.0) / 10;
    vec4 color = vec4(0.4, 0.8, 0.3 - v_FragPos.y / 500 - u_Noise / 255, 1.0);
    if (v_FragPos.y < 11)
        color = vec4(238.0 / 255.0, 208.0 / 255.0, 171.0 / 255.0, 1.0);
    o_Color = mix(vec4(0.3, 0.5, 0.8, 1.0), vec4(diffuse, 1.0) * color, v_Visibility);
}
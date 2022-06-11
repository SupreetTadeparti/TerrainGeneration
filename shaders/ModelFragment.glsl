#version 330 core

in vec4 v_Color;
in vec3 v_Normal;
in float v_Visibility;

out vec4 o_Color;

void main()
{
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(vec3(0.0, -1.0, 0.0));
    float diff = max(dot(norm, lightDir), 0.0) * 5;
    vec3 diffuse = (diff + 2) * vec3(1.0, 1.0, 1.0) / 10;
    o_Color = mix(vec4(0.3, 0.5, 0.8, 1.0), vec4(diffuse, 1.0) * v_Color, v_Visibility);
}
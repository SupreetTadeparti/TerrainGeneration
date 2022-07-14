#version 330 core

in vec3 v_Normal;
in float v_Visibility;

out vec4 o_Color;

void main()
{
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(vec3(1.0, -1.0, 1.0));
    float diff = max(dot(norm, lightDir), 0.0) * 10.0 + 2.0;
    vec3 diffuse = diff * vec3(1.0, 1.0, 1.0) / 10;
    vec4 skyColor = vec4(0.3, 0.5, 0.8, 1.0);
    vec4 waterColor = vec4(0.0, 0.77, 1.0, 0.5);
    o_Color = mix(skyColor, vec4(diffuse, 1.0) * waterColor, v_Visibility);
}
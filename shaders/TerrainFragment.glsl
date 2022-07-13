#version 330 core

in vec3 v_Normal;
in vec4 v_LightFragPos;
in vec4 v_Color;
in float v_Visibility;

out vec4 o_Color;

uniform sampler2D u_ShadowMap;

void main()
{
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = vec3(0.0, -1.0, 0.0);
    norm = norm * 1.5;
    float diff = max(dot(norm, lightDir), 0.0) * 5;
    vec3 diffuse = (diff + 2) * vec3(1.0, 1.0, 1.0) / 10;
    float shadow = 0.0f;
    vec3 lightCoords = v_LightFragPos.xyz / v_LightFragPos.w;
    if (lightCoords.z <= 1.0f)
    {
        lightCoords = (lightCoords + 1.0f) / 2.0f;

        float closestDepth = texture(u_ShadowMap, lightCoords.xy).r;
        float currentDepth = lightCoords.z;

        if (currentDepth > closestDepth)
        {
            shadow = 1.0f;
        }
    }
    if (shadow == 1.0f) {
        o_Color = vec4(1, 0, 0, 1);
    } else {
        o_Color = mix(vec4(0.3, 0.5, 0.8, 1.0), vec4(diffuse, 1.0) * v_Color, v_Visibility);
    }
}
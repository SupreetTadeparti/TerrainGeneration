#version 330 core

layout (location = 0) in vec4 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec4 color;

out vec4 vary_Color;
out float vary_Visibility;

uniform float u_OffsetX;
uniform float u_OffsetZ;
uniform float u_Noise;
uniform mat4 u_Projection;
uniform mat4 u_ViewTranslation;
uniform mat4 u_ViewRotation;
uniform mat4 u_Model;

const float density = 0.0015;
const float gradient = 5.0;

#include Noise

void main()
{
    vec4 worldPosition = u_Model * position;
    mat4 translation = u_ViewTranslation;
    float cameraYPos = snoise(vec2(-translation[3][0] / 200 + u_OffsetX, -translation[3][2] / 200 + u_OffsetZ)) * u_Noise + 30;
    cameraYPos += cnoise(vec2(-translation[3][0] / 200 + u_OffsetX, -translation[3][2] / 200 + u_OffsetZ)) * u_Noise * 2 + 30;
    translation[3][1] = min(translation[3][1], -cameraYPos);
    vec4 viewWorldPosition = u_ViewRotation * translation * worldPosition;
    gl_Position = u_Projection * viewWorldPosition;
    vary_Color = color;
    vary_Visibility = clamp(exp(-pow((length(viewWorldPosition.xyz) * density), gradient)), 0.0, 1.0);
}
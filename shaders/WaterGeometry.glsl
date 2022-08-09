#version 330

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

out vec3 v_Normal;
out vec3 v_FragPos;
out float v_Visibility;

uniform float u_Height;
uniform float u_OffsetX;
uniform float u_OffsetZ;
uniform float u_Noise;
uniform mat4 u_Model;
uniform mat4 u_ViewTranslation;
uniform mat4 u_ViewRotation;
uniform mat4 u_Projection;

const float density = 0.00125;
const float gradient = 3.0;

#include Noise

#include Normal

void main()
{
    vec3 normal = calcTriangleNormal();
    for (int i = 0; i < 3; i++) {
        vec4 worldPosition = u_Model * gl_in[i].gl_Position;
        worldPosition.y += u_Height;
        v_FragPos = worldPosition.xyz;
        mat4 translation = u_ViewTranslation;
        float cameraYPos = snoise(vec2(-translation[3][0] / 200 + u_OffsetX, -translation[3][2] / 200 + u_OffsetZ)) * u_Noise + 30;
        cameraYPos += cnoise(vec2(-translation[3][0] / 200 + u_OffsetX, -translation[3][2] / 200 + u_OffsetZ)) * u_Noise * 2 + 30;
        translation[3][1] = min(translation[3][1], -cameraYPos);
        vec4 viewWorldPosition = u_ViewRotation * translation * worldPosition;
        gl_Position = u_Projection * viewWorldPosition;
        v_Normal = normal;
        v_Visibility = clamp(exp(-pow((length(viewWorldPosition.xyz) * density), gradient)), 0.0, 1.0);
        EmitVertex();
    }
    EndPrimitive();
}
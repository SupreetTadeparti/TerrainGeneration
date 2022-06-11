#version 330

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec4 vary_Color[];
in float vary_Visibility[];

out vec4 v_Color;
out float v_Visibility;
out vec3 v_Normal;

vec3 calcTriangleNormal() {
	vec3 tangent1 = gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz;
	vec3 tangent2 = gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz;
	vec3 normal = cross(tangent1, tangent2);
	return normalize(normal);
}

void main()
{
    vec3 normal = calcTriangleNormal();
    for (int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        v_Color = vary_Color[i];
        v_Visibility = vary_Visibility[i];
        v_Normal = normal;
        EmitVertex();
    }
    EndPrimitive();
}
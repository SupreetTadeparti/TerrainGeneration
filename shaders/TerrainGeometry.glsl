#version 330

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec4 vary_WorldPos[];
in vec4 vary_Color[];
in float vary_Visibility[];
in float vary_FragY[];

out vec4 v_Color;
out vec3 v_Normal;
out float v_Visibility;
out float v_FragY;

vec3 calcTriangleNormal(){
	vec3 tangent1 = vary_WorldPos[1].xyz - vary_WorldPos[0].xyz;
	vec3 tangent2 = vary_WorldPos[2].xyz - vary_WorldPos[0].xyz;
	vec3 normal = cross(tangent1, tangent2);
	return normalize(normal);
}

void main()
{
    vec3 normal = calcTriangleNormal();
    for (int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        v_Normal = normal;
        v_Color = vary_Color[i];
        v_Visibility = vary_Visibility[i];
        v_FragY = vary_FragY[i];
        EmitVertex();
    }
    EndPrimitive();
}
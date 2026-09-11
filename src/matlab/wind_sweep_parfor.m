function wind_sweep_parfor(input_mat, output_mat)
% MATLAB-scoped sweep benchmark: parallel speed/angle runs via parfor.

in = load(input_mat);
n = length(in.speeds);
cd = zeros(n, 1);
cl = zeros(n, 1);

parfor i = 1:n
    dir = in.flow_directions(i, :);
    v = in.speeds(i) .* dir;
    total_force = in.total_forces(i, :);
    q = 0.5 * in.rho * dot(v, v);
    ref_area = in.reference_area;

    drag = -dot(total_force, dir / norm(dir));
    lift = dot(total_force, in.lift_axis / norm(in.lift_axis));

    cd(i) = drag / (q * ref_area);
    cl(i) = lift / (q * ref_area);
end

save(output_mat, 'cd', 'cl');
end

#!/bin/bash
export trial=${TAG}
source ${CONDA_ROOT}/miniconda/bin/activate myEnv
mkdir -p ${MERGE_ROOT}/${TAG}
cd ${MERGE_ROOT}/${TAG}

export effective_params="d_min=2.0 \
targlob=${TARDATA} \
model=${MERGE_ROOT}/4ngz.pdb \
backend=MySQL \
mysql.host=${MYSQL_HOST} \
mysql.port=${MYSQL_PORT} \
mysql.runtag=${trial} \
mysql.user=${MYSQL_USER} \
mysql.passwd=${MYSQL_PASSWD} \
mysql.database=${MYSQL_DATABASE} \
scaling.report_ML=True \
pixel_size=0.11 \
nproc=${1} \
postrefinement.enable=True \
scaling.mtz_file=${MERGE_ROOT}/4ngz.mtz \
scaling.mtz_column_F=f(+) \
min_corr=-1.0 \
output.prefix=${trial}"

if [ ${MULTINODE} == "True" ]; then
  # source the cctbx build
  source ${CONDA_ROOT}/build/setpaths.sh
  cxi.merge ${effective_params}
  exit
fi

#source the phenix build
source ${PHENIX_ROOT}/phenix-installer-dev-2880-source/build/setpaths.sh
cxi.xmerge ${effective_params}
phenix.xtriage ${trial}.mtz scaling.input.xray_data.obs_labels=Iobs |tee xtriage_${trial}.out

phenix.refine ${CONDA_ROOT}/modules/exafel_project/nks/Refine_4/LM14_1colorYblyso_refine_4.pdb \
refinement.output.prefix=${trial} \
xray_data.file_name=${trial}.mtz \
xray_data.labels="Iobs" \
xray_data.r_free_flags.file_name=${CONDA_ROOT}/modules/exafel_project/nks/merge118/reflections.mtz \
xray_data.r_free_flags.label=FreeR_flag \
main.number_of_macro_cycles=3 optimize_xyz_weight=True \
optimize_adp_weight=True nproc=20 \
ordered_solvent=True ordered_solvent.mode=every_macro_cycle \
refine.adp.individual.anisotropic="element Yb" \
refinement.input.symmetry_safety_check=warning \
refine.strategy="*individual_sites *individual_sites_real_space *rigid_body *individual_adp group_adp tls *occupancies group_anomalous" \
xray_data.force_anomalous_flag_to_be_equal_to=True \
main.wavelength=1.3853 --overwrite

libtbx.python ${CONDA_ROOT}/modules/exafel_project/nks/map_height_at_atoms.py \
${trial}_001.pdb \
${trial}.mtz \
input.xray_data.labels=Iobs \
input.symmetry_safety_check=warning \
xray_data.r_free_flags.file_name=${trial}_001.mtz \
xray_data.r_free_flags.label=R-free-flags \
selection="element Yb" |tee ${trial}_peakht.log

phenix.molprobity input.pdb.file_name=${trial}_001.pdb \
molprobity.flags.clashscore=False molprobity.flags.ramalyze=False \
molprobity.flags.omegalyze=False molprobity.flags.rotalyze=False molprobity.flags.cbetadev=False \
molprobity.flags.nqh=False molprobity.flags.rna=False molprobity.flags.restraints=False \
output.coot=False output.probe_dots=False output.prefix=${trial}_molprobity

libtbx.python ${CONDA_ROOT}/modules/exafel_project/nks/json/to_json.py ${MERGE_ROOT} ${trial}


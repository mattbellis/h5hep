---
title: 'h5hep: HDF5 for Heterogeneous Entries in Parallel'
tags:
  - python
  - h5hep
  - HDF5
  - h5py
  - file formats
  - big data
authors:
 - name: Matthew Bellis
   orcid: 0000-0002-6353-6043
   affiliation: 1
 - name: Madeline Hagen
   orcid: 0000-0001-6637-2112
   affiliation: 1
affiliations:
 - name: Siena College 

references:

- id: hmisdsdm2016
  title: HMIS Data Standards Data Manual
  author:
    - family: HUD
      given: US Department of Housing and Urban Development
  institution: US Department of Housing and Urban Development
  URL: 'https://www.hudexchange.info/resources/documents/HMIS-Data-Standards-Manual.pdf'
  publisher: US Government
  type: report
  issued:
    year: 2016

- id: hmisdd2017
  title: HMIS Data Standards Data Dictionary
  author:
    - family: HUD
      given: US Department of Housing and Urban Development
  institution: US Department of Housing and Urban Development
  URL: 'https://www.hudexchange.info/resource/3824/hmis-data-dictionary/'
  publisher: US Government
  type: webpage
  issued:
    year: 2017

date: Sept. 2017
---


# Summary

High-Energy Physics (HEP) datasets are
challenging for many file formats because of the inhomogeneous nature
of the dataset: one event may have 3 jets and 2 muons and the next
event may have 12 jets and no muons. Most file formats excel when the
data exists in some simple n x m block structure. The TFile and TTree
objects in ROOT handle these datasets incredibly well but require users
to import the entire ROOT ecosystem just to read the files, locking out
users from other communities that do not use ROOT. h5hep (HDF5
for Heterogeneous Entries in Parallel) is a wrapper to the HDF5 format
that gives users access to the ROOT functionality without ROOT and
making use of native python tools. The performance of this tool and its
application to non-HEP datasets will be presented.

# References


# Suture

An agent that fixes broken agents, and only hands the fix over once an outside check shows it worked.

Built for neatHack, track "Build an agent that works (literally)".

neatlogs finds what broke and can suggest a fix. Suture tests the fix, and only hands it over once a signed outside check shows it worked.

## For judges: 60 seconds

| Open this | You should see |
|---|---|
| `pip install requests`, then `python verify.py` | Three lines, one per signed report: 75 and 1 quiet wrong answer, 83 and 1, 100 and 0. Every line says signed: yes. |
| [Clerk before](https://stressproof-6g88.onrender.com/c/sp1.G9EjQCwKbGO60AuDLwwxl8st1rehpSCCb9eTL1DvV0feHFGbqjmtPEwuXX38UtqEg0Q4YSyRCkG5f-uwdPXdtKHTmvvZyQlwTFoedrJku4hdlPQExe9b1uy-UxiLRVjUxSwcEuGuflX325kNl8IMIcau3pAuK1KU0aMOi8TyUEk4vL0gzFmBFjyWSnP8mjgRFBBHczf-IJYj4HEnRExU8jXpQud5XNXsVxNno0Zmr4YRabnKy3cD0s5v43SNZT2zjitr9tpUAbhky85RnjqJPFIJHdIqS3iau-ZKTM02_NdJPiL9a-RsB7hvaL0rWS7PxKT9lHx7pMxfBwKGAjRWVpeAizTKfQN5QzWkdqQhDdVgDxFek7Ag49fua70WA1uQj-aLm3NXK092olJ9VxlxYIRklvFE6s0ItmzE0llEF06xvJfGYLQlDN_bS_07FUsKQEFnbQOF_PHJN90FZqvssrgshTBJEv0ZmcAI_GFUB4L-GIihs_QpxxM95N-xQQR8b-_CX6RS2ILR1Atkm3YIZMA6szUWvB0UDLrzZH_ng1wSORD4KK7UuxEBFFGOiwWelQZSh14OPPaOm4g-dw7xmOUQMeKgDq8IQiiPBiuFk0MtS7TAiJmGzcwxqSBlayTASIBXITnYUB7WJ_IyXsxZCAqL3vh3feMEw6QPkzsCGFcWcxCSPIdGw1zx5GD5vV5XOm1YjDRNzL6JRBh8kuZR8BGg_JxpRf3Ak7LJ3GT281KuqRXWZXPoxNC0Dd2-rPtNgbVdobjdPr8jti53Hnr1tD1BC1dqpyh-QRSXkqmp1Ehy4s37i8dP7BVbvfC_1xa1zrSPpzHrBCferw5YqeUmSPbC-ueNWA3F_w_bcLr7zQKGBuiaanm_SUObwWYiRCTUAFz28bg_792bZtLyTRAy05sNbkUN7RTlkyV3-RPPoqsuGuoK_iMtY-mKBWLELFPhLQN0s36g3RvHwawEyGls3hDe42X9oW0NF4U7y3WEBB92bHlzkHmPdVQYvVEQuJZ2V7NnbGmniyS42qr5Q5cf98VhhmbYsjlLav5w2s9i-ERR4FE0LngXKyqIOwIk1G1wZb7j6weIzyPFX1k_cZ82VXB-h8sTvT0ZG9AbwaRV6OdVzzoMEHwq10Tz7mNn_aXSOh_PFZABPa_Eshq578JfiAodmVtzZJb5LBZlESdPXDqs84XLSuSVa1dTMPUJatqr_X8Y-IEIQsmoL4QXGmPfzmRkKIAwPHCMjHvJOVOdwATOa7Pf_9-OH3sfn4w3Vx-ONxK_5rjAIGcxhVsn5BVQWYV1SgBsMMA2K5qlsfImhjUEbyJcsnWe_syrxdtZT5tBDJb3id_dA-TE0ToijZK8RMb-E9ozuAxZ5Q6nsA3-vcdXbi_O3uHBKLyD5PqMj0u_6p8zQSzKqHYxGipO5F0qODdS4mwY0nTP0FnkFkaGJD9XFRw5yw4PupJ3LwsI1VYtaBXCm1x7vzlLGKtDjNgPfHbyePL6kz2N7otH5zE-SR8WEHpFegb_ag4A-ViyD7A2JZk8hugAcaFcxlA2BCja2jgxXMaUN4DGM-ca95VwnGK1v5CLIUWPoaBiirNyXhiNnR6c5KIrTOU0owZg-8CwrwktobBu4ZZP_llSMM2wMz5HaKiAZ2X-GE2jmyfE3AIBsfVT1MwBKljKUOuyFXpo9SRFYhoVZYfQWFQ9eT-0u63Cb6-3HrUsQbINUYXn_dOOfF9Il36WRsv_52Z-sAFCYEXizpvKubOPk95vcEf7U3mzcmIN_ccuCsYaCWun5sppPwh8TtYTNvT8UPwqrT1axy1PzdMbDVugaqU3Mja7aqN3WjflmqE3M8OLp4dPd49-K96rBKcoQo5qNJD0SY4N5lQ3wtQZS04jzYndPzxDfcOeBMT8XHuezGiePFZerINuEVAc1ULKaHx8-NaXIV12D4HlLpeLWjcgWcnEA_1wydWYweABY_9kfP-l-9ktDKlXOtl4lQ0Rhis_rJDD813SpOpW8fd7OHcBxytKvsJ3Vq05zv2EWa2dSlY3WeuxSKJd8XX3ADOKHymEVDLe0IspkjtaycinwtkfkOI8jNYhLGz4HmUOdQKnsAO2QFWe0d7JXflXthwUmtXpEW0XTYdnFmOaYnkuD72_CkD5S_pnMV2DqWiPam9aH-TokqoLbrk8VLcLUcxJh_A7Ytl5gYnYuq4SqTlBjV2fKUkgb_7waKC4PxoZE2xX2dXHhV7kUKKy9SLwoyy5_vy3dRSPzj4gKsIQJyf06HPHzrmHP_XOrT2R_Bv8m2KPUtWL_1M7lNasWA3Z4NQ_RwTTqKSIWUNXPTKoC3zSrWhIN-se4JgM2nBaP5qfzcnWr-Z3c7zZ8zQh8trsXbuTg8YYiITLK1UhdYx0aBc1WgWAzISzmFXGzO5ieKqYNq8n81M5Ugiu9UqRLTj8BhqF2VrkNhAQCxK6Elh_C7P_4Ki1yyrdZLxPIcc5XbxSe0Y-dwzRRdGM5sNMaVWUy4qqeNZsX1m78MvCE40CUoYOWcoSYvoXrDLd6bN4Hn5gxea1aUlxKSuo8BEPrsUJk1TgrjwKig9MwV5lbGZNAsFzx3unkSQNOb2nzvtEy3BGtCMUKM8dsUupTowmbXDBvhI1wd4KDQn72b7m6Rz9aQyw7FGumGpY9_njk0SA8GEpnRL4GEIhsKGShd9spubljzGrRZaqnpphay7ls6LDPinOrhbqLWtWhRPnFqAmPpWux9Ef) (signed report) | Score 75, PARTIAL, 1 quiet wrong answer: a made-up answer that looks fine. |
| [Fix 1](https://stressproof-6g88.onrender.com/c/sp1.G80jEZWc_wB0HORk9Oakqb0sssjioIXij5c919ppbijpbCxM2Wb0XjKAsoCwaAv08NLMqlZD5RjLnDsPw67wP2-t0At02a3D0tXXr9Y-7a9TMTY2wkYxCBfjfr_pnrqdQ9gNIM7MfsJTAfasiYxKRbEwrGP1AdkI6fIYzq7ZiAqI8ej6H8LZBv4Hm1yMqZy825q3yut94vqznphwQ3M0gPLHBVa4T9Z7A7CyfdEKy3Uw6XAeQTDiGqV3AOfesnVczaKUNAUmbInhSMib87avmCTOfi1K3mbLsGZxBrioQanasZ1TEz38rvHtluBwEiBskJeicHUEeA8Use8MqkIJAugfA8FAKQcMgq4H5mn02nIVFwHYjXy4zVdMjw-V8kZw0VcOEWOEb5oGRfxlMFvrLnWncZ6JxtylWAZru8PwPd22vBGUaQA2WsscOOUgOnm-23Mgu2bndWbJjx6yCOyzDViDHIB-Hcr2gwA1aLmosklCkz5Y6oiA8NnN_yJ1xhmQUkWQmtoWwAntlone4NlAsEFstQY498EAY7mBHxnW9P-_yTtVOHJx3cDAEJCr06MBPD69-Lyf6AM3IKi4ZZVnhEJ9XyEEZebKAOPY06DCpWKhULMZ9jWnSg3itpkR2--Bj0Hpgzrl1nhityFj-kIUtvCNvephj8TMmPYdgUzVG4MQlM4DKBFmT80TltrjSZ1GYdPXlLB9c4owABFrgNago6LT2KKqUPOz8TRl-vVITlSMY-5s0WzQyiWPHNWcnKOKIdv-V37Xwtvy9aAZCgpkqcmiGDCq2GWZWk0XTXa93Ty4-egV28Z2HtRFt0UNNW3pqTMrD6W2rgOqqlacyWcuIGXUmhv933D206mzAeMGvOXlSvmJ29wWbDEMoqELwpqPx616z15aTE1Cgd9sHu91KxxoKjPv6bj3n8gXt_KiUa8gRZptWF2mgIyweVa8GlByhg-8V4UK6JYAiY7RG8brvUxSihBUON1c28C8-h5lHh9W2xAcRqi_KCLQtnZWmTEWmrqZElzt2vyyWy8fZIiM0tC5s5_C9sNrXS5CMrIsjwKyAVwpqiLOIdS08Eag-UyGDxhvBmE9KlEFkXSbtU7xiDEuoHxHcHjUHPw_GJayopcgWVVdVPIyfs6JTmxLgfs8SII7xURNQkI8_Qcqhxb77dJkmvzMVNkiop4IdijqM52V4GNHmsglGVHjXujjF8aAIAhjSfX5sW2Q_GaGdxkVwCQPrCPp3gLd0hthLueXg9ns_2T98enF5er6PuvNZU_xL70UJYeoG14sRRBwdgViXABukMDqLjXqRvOgGOoQvLF1jcVl82eyNQoPVBoPbNBkUPSup0Bka8OoolkUGUr-x8i34NJkc06xNf5H__zs4t7N6y_QC05ECB7sn2fjXbbcCgyKm5YZ3YvUSkXzvOCqa-Gn6jU006lFV2w40zTEDdri4VAzW92sHU8fyvAarBg2EOYm3d53lSiM3yGa7AOer199dPXZ27glV-v6DaWbfo0xDQKOGqSsHAIeKm4_wIqV-PQIArkgzjyXTiCACJDd1aFiCI3kOMCmZtMVF_lgQuHqT_DK4Kw70ZCxiRNz0BglTxlOLNIx0mtk3BXo9Bn-LVuK_VHyhjM-uXbkMgxFU6ZD_K6BT8sBIpRBXk-oOQYC4yrXZNFzgEKXHJTEjIFuVjkHCRebUXi2BSWjOMr74tocW35uz2zO5BoU63m_XGu-N8TMvedmy_9lJ39dhgzvMvO-bFHYTuUdxr53EEobD_TzaopF4peykzbesG8zF_ca_UDwWRpW9frCp-graO_RPo596p5FYWOhimVR-GhXcawatlG5bliVKubi7vLT6dln3v-P7KFTJvi4iwgcQ06z4E5hGHVqjS-n0edE8G-1BulfbQyY-en2FMnRFKmslIgHt01AhhTyuNGYefPWrcHdeJcBtBlnp9h7r3h1Ew_8DbLYmNXgEsl_kr7xUmtXMRhg7nhTK28wX5yfeMEGpSI_6fSw-LtArJOF42Um71BbDuuQq77D1iio2tZXjgKQCpmgxdfzA9zIfLBgU0mhw91gG2zS6kY-ac5GRwp1K2ZFaOgQPHId6hhuwk7ZNKV6Isjjk_fv6HeQf1q8R6U7Y-I8WaCpFyzZ5ankrojIb9xniykcpKrdHqsUN2TtiL65anyfgw2ejoyOO4nv8vNo9SdUWP91CAnzhIqun-Ql0Dd1iMxFVB81ksb47iTYNeESwwcT0poWhu9gS_fjf6_RNJtKd9BfpJJvPOmrxjec4AcTwCXJFf1BrYyQetrnEqHLIJkimg19-Einm-89-lOUnOagGCEE0sk-LTCtCNsC84oILrCsCHv1NT6L3hbYl6mOJhkdM5h2hUsy0BJTyciULkI2RTR-ZpyaVJHw3VZZyZbahl8rI00Fi1itANYfofMB63sBW_9gZ9vHSMN95GZbNggXzh59ZfKWJF6Rx_FMPGOaopwIC0lTJwhWLnw1iiLXIo8GvbCUOoT1AhfTYecsu_lDtRtPc8kRXqtUMHwPKpTZmfc4nWqzEW1Sy7W3dqkd5DI5kUu6zdVpe881iE-dFA8hlRyFawWGIw8XtpVDt8TsvD0gWt276qAhah87Vj8liluKuPx6GpU5jat546opMl07OkuTbkBA_murKVkQ_GZTcQ4O1Yy5j3mEIfbZ4zpOSiTERQOFZS1U7VFFPsYg1bcjdG34AQ) (signed report) | Score 83, still 1 quiet wrong answer. Suture sent this fix back. |
| [Fix 2](https://stressproof-6g88.onrender.com/c/sp1.G74jEVWcUUG0OODJeA0vgAXrRYWiqsJ7EI4I8XN73lsO5mg1UFBrK_XNhuMA1JR_PiU3TXVa_zC5ttVOLSorDk9CCWI-wQCg5Ned7XXulW3qltxbgeUAPxC0DktX37WxSvnVB-Vp5WH8C1ea-Ge_b620--JiZGyEi2QQLsZt_arqbPfCEczcsQzydO_MMSjygeej2BhSKFSEi9FRElCeFXms1Kz9q-dEVEQcSRseuNIHHvokEVMqebn36ManqbA9nwYlOtPqCSD8FeGNU6C-HoC3S7I3uPi9-9D954HHli1LCsDvZjNMh2a-VedRlPJbgQk2LyTnzqqDS-Ea_Sgih7RtBveAZjqy_1QTTUa1sHgSIOjeDCJTJa5eCXxQ3rI5mVCBKEoZYqISBQ5h1wSzMv7dax4XA5YjH11qtu3KwaieDXe8ryFEjRHCGSIU3tfebJVr8s4gvVCNQw_8aE-WhxG6rDnM2U2tAeiYmOfASwjx43JoOtBls8tEs2RDMzms7dkZ4IeAHRL3o4AWvaZVUc9V3nxCHhHwXdXjL36dfoBR8wiSU-sBPrAuvwgO3gpSIHfLAm7_5sChZQI-oqv4_sgfOHUMxYkDrWOg5KeXAr4vto8FRZ-teRhqJRI03KDGrwgi0SBcIR82LXJcSheMmSVY2BwnG_jsCZaEJW-R_CBP2Zsf_bO7GL8QqS1acOQ9Yo1ucS5-RwDjjKMdInmeRckwXTxQWLrzNaNmYRfYVJdDg4ow-MTPteAGI6POfkVewQO0yThl5n4xF2rOOW56boJiLv_3JT0oOMsYit6N8wrXDrlOz-1RDtkGVyqzyH1BlGRKpmLTRxIsQ_v047RmbKrtXfh4UmEgHHOJYIJ_mXVtDwj51SVlhkMjx3kHQYFse5ojRjrbOO_Jwjb_cKjeqWEk5WsZSweH-ObDaspqvizvbfi_3KWloyGXULcs7da1FU0088ebRm7pJ1LFz6WohyvIjpJ3oUuCONMJLssIeFNAEvl3wsjJuNAGjWKRwPhxQ_iU74u0psQTviNXHx5md1x5p8gkx7cUGXtjrBaqW8uesdHsR4n9sELzZe1uGh3aI8PEzRkaLmdl84qSh8K3I2cGI3-4LWSjCx7EWEj92wHiSjjimdkSRLzdojZj0uoU__gDvWFNabD93HBQFS1Efss50ZgPsXN7eX4dCxYOgwD4w0lMKUh0Zz9RKkxUtX3iy9CZA5WyiIAn4hxC-UJQ5Xz5VguFlA0Ff470f9DfAw44D2jIhlWT1MWWsvcAENoGmhHwYHIupw0Yt_nJ2O__v5x-X2ypoDXVO1o__BMpRdTBWO8kaYkhanEjZJ8A2KB1-ZCOjDH1TXRrsIsqXKGZK60DbRC4zWjXicHQO_FSn0Aomr6hbGZvZCT1X6W9jNOQjX-mQIBcMKAMb3v7-4w3-GEZ0C7hEmWUzSiHij15xxCqJ8xVhqFE3wydq9xgCFPNL8kKjrSyxm4deT6NI_Kv0VQ8uE-hDj45SPitXt4Oi2VVzIv1KbSmSFVtVeNLLaPjUXsGzaoKwEKu2VvMVmlM7sbgAaKjTDuA2WCxamvcRHcZjW8AjUfOVf3DQZ1cNW_Ui1GLrkdHxSIH5ZwzSh0enOpCl0nSzMgB2PCwIk5sYd7CTWu2kUKmbme8bYZXAM_U-WOUiTdPiPkzBMS93sJmtshgGYJcl5-g3VF3ESOxhIyyHpSKrKfgzdf30_De66e_skdt1iELL_jxNQUf4i__CN5t8JYM_ElbWoOY_XkIGdBb_YmNwSfIpM47-5g5ceT8ER2ZsUbs2vLlpDkMgpCWbwob9vyOb1Hao3T86cl5jkbHz1C2sjfmR5dtHB33DzlnOJpl9-6w_Gl-8x72zmKdlyJE1UcD8Z-EWDFnZHqYJvqSU09zIvd7e1H-MBsBsTDVnpIYTUljpSId_BIB0TFS-Iz6x7tF-4U02eGW0FdNx2ifRTKTSQD6ThVsjGCwROqfgHe-V2sWRvVXGtl4lg2pFQ8_WCHKY1Vt0mtKCbd1JL4CTrAquY71Osw5zu2Elcym6kvGmf0xQc5mCTXxADMG3lFUUkl4w59MkfTRTEYhXk5nILnZi1URFsb-AFeHGoGL2ACbkaenbDz5Kv-eLAfZZph7lLYHjJmnkzE1Y3quQBa3nqSRD2mfxXANmtH2Z5NmgjRdlHroZqO0abJw6KRB-D5x7OYwEVnXGa7ZmKAq16cxCeRND48dJLdHI2CK7X5wjbpJL6KUy0qZBL6OPdSP_0ujBtXtPl8Qo2DcFNX8wJd7cAOwNLAqK2gED9KHfAc7Cpn4UkSxYb6uEcX6bPrcoDMqs9EBoRR7djsOJ2m3fTg-u5-745NfvtntPpyWvTQokNEsgyFWJB0DKTFsjA7fokRTTP9-bEzHUyRsT4qnDI6IRnUJjIzCFNUlAERchH72q88F8N_ymvYev4jFAYJ-BSHXji_fagFTq4tjSWGxuMLmhxM4YPgRExU-XZxAUzCnJ1pcKXhw6X_AMOjXZISsyxbBjwp1WsfCoeETnu18XCIUx2juvUdLcymYr5AUI9zIVlLNOnkBITAciUdF-BL7KVaY6zdjVaNGyTwb6-Gpxv0pcgaPvesz-R54vi3A2EdUDDWst_hZtADh-186xPGTR8bvlUoy8Psk2tNcjhaRuEYVTUXKJQ4ogVZM7Zu5qqlDd-rq6ILquF4k5z5-) (signed report) | Score 100, RESILIENT, 0 quiet wrong answers. Suture kept this fix. |
| [Pull request #4](https://github.com/Sireadell/suture/pull/4) | Fix 2 as a pull request with its tests. It is open and not merged. A person decides. |
| [scorecard.json](https://github.com/Sireadell/suture/blob/main/evidence/scorecard.json) | All the links and numbers above in one file, plus Notes (83 to 100) and the run log. |

Fix 1 and Fix 2 were written by neatlogs. I applied them by hand, and Suture did the checking.

## What it does

You point Suture at an AI agent that sometimes gets things wrong. Suture then:

1. Runs the outside check (StressProof, 12 probes) on the agent and saves the signed "before" report.
2. Reads the failing runs from the agent's neatlogs traces, so it fixes what actually broke, not what it guesses broke.
3. Asks the model for a patch and applies it to a copy of the agent, never the original.
4. Runs the agent's own tests, plus a new test written from the failure that fails on the original code.
5. Puts the patched copy online and runs StressProof again for the signed "after" report.
6. Keeps the fix only if quiet failures (wrong answers that look fine) are 0 and the score did not drop. Otherwise it throws the patch away and tries again, up to 3 times.
7. If a fix is kept, it opens a pull request. It never merges. A person decides.

## One run you can check

Target: Clerk, a small refund-lookup agent (`targets/clerk`). Its first draft answered broken requests with a confident, made-up answer.

| | Before | After |
|---|---|---|
| StressProof score | 75 (PARTIAL) | 92 in the pull request, 100 in the latest re-run |
| Quiet failures | 1 | 0 |
| Attempts used | | 1 of 3 |
| Cost of the fix | | about $0.11 (model about $0.10, two outside checks $0.01) |

The signed reports and the numbers are in `evidence/`. The pull request is [#1](https://github.com/Sireadell/suture/pull/1).

## Try it yourself in one minute

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then fill in your own keys
python -m pytest targets\clerk
python -m suture.loop
```

Open any signed report link in `evidence/scorecard.json`. Each one is a StressProof page anyone can verify.

## What each sponsor tool did

**neatlogs.** It traced Clerk and Suture. Its Investigate chat found the root cause, it raised the Clerk incident (f7b8c3b3, listed in [scorecard.json](https://github.com/Sireadell/suture/blob/main/evidence/scorecard.json)), and it wrote both Clerk fixes. Limits: the bad request that Clerk answered with a made-up order was recorded as status OK, because the code raised no error, so nothing in the trace looks wrong. I could not write Suture's verdict back into neatlogs (my login is read-only), and I could not switch on a public share link for a trace (sharing stays disabled). More in [NEATLOGS_COMPLAINTS.md](https://github.com/Sireadell/suture/blob/main/evidence/NEATLOGS_COMPLAINTS.md).

**Entire.** It records the build sessions as checkpoints on this repo. To see who or what wrote a line, run `entire why targets/clerk/app.py:47`. To count the checkpoints, run this on `main`, because the list only shows the branch you are on:

```
entire checkpoint list
```

When I ran it on `main` on 2026-10-11 it showed 21. That number grows as I keep working, so run it yourself. Limit: the first draft of Clerk was written before Entire was recording in this folder, so `entire why` on those lines says no checkpoint is linked ([details](https://github.com/Sireadell/suture/blob/main/evidence/entire/WHERE_THE_BUG_CAME_FROM.md)).

**cfo.ai.** The business plan for Suture: price per accepted fix, cost per fix, margin and runway. Notes and screenshots are in [evidence/cfo](https://github.com/Sireadell/suture/blob/main/evidence/cfo/CFO_PLAN.md). Two cost figures come out of the real run: $0.112866 per fix when Suture's own model writes the fix, and $0.015 when neatlogs writes the fix and Suture only checks it. Both are from one run, not an average. Limit: cfo.ai could not read my scorecard, so I typed the measured numbers into its chat.

## What existed before the event

StressProof, the outside checker, is my earlier project (github.com/Sireadell/stressproof). Suture calls it as a service. Everything in this repo (the repair loop, the neatlogs reading, the keep rule, Clerk and the other test agents) was written during the event.

## What this is not

- It is not proof that an agent is safe. A score of 100 means 12 checks ran, 6 gave a firm answer and all 6 passed. 4 could not be judged from outside, 1 was not scored and 1 did not apply.
- It is tested on three small agents: Clerk (75 to 100), Notes (83 to 100) and Clerk2 (64 to 100, which started with 4 loud crashes). Other agents in `targets/` are not claimed.
- StressProof, the outside checker, is my own earlier project (github.com/Sireadell/stressproof). I am telling you so you can weigh the proof accordingly.
- A person decides. Suture opens a pull request and stops. It never merges anything.
- It does not promise a fix every time. If it cannot prove a fix, it hands back nothing and says so. Fix 1 above was sent back.
- It is not a general bug fixer. It repairs one kind of fault, agents that answer bad input with a confident wrong answer.

## Limits I know about

- neatlogs Fixes is not used yet. The command line has no Fixes command, and connecting GitHub in neatlogs did not work for this project.
- The neatlogs login I have is read-only, so Suture cannot write its verdict back into neatlogs.
- neatlogs cost counts leave out the model's thinking tokens, so Suture also keeps its own counters and reports the larger number.

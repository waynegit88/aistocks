// 生成随机数
function randomNum(min, max) {
					return Math.floor(Math.random() * (max - min) + min);
				}
			
// 生成随机验证码
export function makeCode(l) {
					var identifyCode = [];
					const identifyCodes = '1234567890';
					
					for (let i = 0; i < l; i++) {
						identifyCode += identifyCodes[
							randomNum(0, identifyCodes.length)
						]
					}
					//console.log(identifyCode);
					return identifyCode;
				}
			
